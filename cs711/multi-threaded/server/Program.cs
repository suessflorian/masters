using System.Net;
using System.Web;
using System.Net.Sockets;
using System.Text;
using System.Text.Json;
using System.Text.RegularExpressions;
using System.Text.Json.Serialization;

public class HTTPGameServer
{
    private static void mux(Request req, ResponseWriter res)
    {
        try
        {
            switch (req.Route())
            {
                case "/register":
                    {
                        var player = GameState.CreateUser();
                        res.Write(JsonSerializer.Serialize(player), HttpStatusCode.OK);
                        return;
                    }

                // shape: /pairme?player={username}
                case "/pairme":
                    {
                        var parameters = req.Params();
                        var requestingPlayer = parameters["player"];
                        if (requestingPlayer == null)
                        {
                            res.Write(JsonSerializer.Serialize("must provide `player`"), HttpStatusCode.BadRequest);
                            return;
                        }

                        res.Write(JsonSerializer.Serialize(GameState.PairUser(requestingPlayer)), HttpStatusCode.OK);
                        return;
                    }

                // shape: /mymove?player={username}&id={gameId}&move={move}
                case "/mymove":
                    {
                        var parameters = req.Params();
                        var requestingPlayer = parameters["player"];
                        var requestingGameId = parameters["id"];
                        var requestedPlayersMove = parameters["move"];
                        if (requestingPlayer == null || requestingGameId == null || requestedPlayersMove == null)
                        {
                            res.Write(JsonSerializer.Serialize("must provide all `player`, `id`, and `move`"), HttpStatusCode.BadRequest);
                            return;
                        }

                        res.Write(JsonSerializer.Serialize(GameState.MakeMove(Guid.Parse(requestingGameId), requestingPlayer, requestedPlayersMove)), HttpStatusCode.OK);
                        return;
                    }

                // shape: /theirmove?player={username}&id={gameId}
                case "/theirmove":
                    {
                        var parameters = req.Params();
                        var requestingPlayer = parameters["player"];
                        var requestingGameId = parameters["id"];
                        if (requestingPlayer == null || requestingGameId == null)
                        {
                            res.Write(JsonSerializer.Serialize("must provide `player` and `id`"), HttpStatusCode.BadRequest);
                            return;
                        }
                        res.Write(JsonSerializer.Serialize(GameState.GetOpponentMove(Guid.Parse(requestingGameId), requestingPlayer)), HttpStatusCode.OK);
                        return;
                    }


                // shape: /quit?player={username}&id={gameId}
                case "/quit":
                    {
                        var parameters = req.Params();
                        var requestingPlayer = parameters["player"];
                        var requestingGameId = parameters["id"];
                        if (requestingPlayer == null || requestingGameId == null)
                        {
                            res.Write(JsonSerializer.Serialize("must provide `player` and `id`"), HttpStatusCode.BadRequest);
                            return;
                        }

                        res.Write(JsonSerializer.Serialize(GameState.Quit(requestingPlayer, Guid.Parse(requestingGameId))), HttpStatusCode.OK);
                        return;
                    }

                case "/debug":
                    res.Write(GameState.JsonSnapshot(), HttpStatusCode.OK);
                    return;

                default:
                    res.Write(JsonSerializer.Serialize("not found"), HttpStatusCode.NotFound);
                    return;
            }

        }
        catch (NotFoundException e)
        {
            res.Write(JsonSerializer.Serialize(e.Message), HttpStatusCode.NotFound);
            return;
        }
        catch (NotYetException e)
        {
            res.Write(JsonSerializer.Serialize(e.Message), HttpStatusCode.Locked);
            return;
        }
        catch (ForbiddenException e)
        {
            res.Write(JsonSerializer.Serialize(e.Message), HttpStatusCode.Forbidden);
            return;
        }
        catch (FormatException)
        {
            res.Write(JsonSerializer.Serialize("invalid requested game `id`"), HttpStatusCode.BadRequest);
            return;
        }
    }

    // handler consumes the clients request and assembles Request and ResponseWriter
    // which will be passed to a mux to be handled. Pattern inspired by https://pkg.go.dev/net/http.
    private static void handler(Socket connection)
    {
        connection.ReceiveTimeout = 10000;

        var remote = (IPEndPoint?)connection.RemoteEndPoint;
        Log.Info($"thread {Thread.GetCurrentProcessorId()} established connection with {remote}");
        MemoryStream memoryStream = new MemoryStream();

        while (true)
        {
            try
            {
                byte[] connectionBuffer = new Byte[1024];
                int bytesRec = connection.Receive(connectionBuffer);
                memoryStream.Write(connectionBuffer, 0, bytesRec);
                memoryStream.Seek(0, SeekOrigin.Begin);

                byte[] written = memoryStream.ToArray();

                byte[] body;
                byte[] header;

                if (written.Contains(HTTPRequestUtil.ContentSeperator, out int endpoint))
                {
                    endpoint += HTTPRequestUtil.ContentSeperator.Length;
                    header = written[..endpoint];
                    body = written[endpoint..];

                    if (HTTPRequestUtil.ParseContentLength(header) >= 0 && body.Length == HTTPRequestUtil.ParseContentLength(header))
                    {
                        var req = new Request(body, header);
                        var res = new ResponseWriter(connection);
                        mux(req, res);
                        Log.Info($"thread {Thread.GetCurrentProcessorId()} sent response to {remote} for {req.URL}");
                        memoryStream.SetLength(0); // clear memory stream ready for next request
                    }
                }
            }
            catch (SocketException e)
            {
                try
                {
                    connection.Shutdown(SocketShutdown.Both);
                    connection.Close();
                }
                finally
                {
                    Log.Info($"thread {Thread.GetCurrentProcessorId()} no longer listening: {e.Message}");
                }
                return;
            }

        }
    }

    public static int Main(String[] args)
    {
        // handlerMem will host everything received
        MemoryStream handlerMem = new MemoryStream();

        // Establish the local endpoint for the socket.  
        // Dns.GetHostName returns the name of the
        // host running the application.  
        IPHostEntry ipHostInfo = Dns.GetHostEntry("127.0.0.1");
        IPAddress ipAddress = ipHostInfo.AddressList[0];
        IPEndPoint localEndPoint = new IPEndPoint(ipAddress, 8080);

        // Create a TCP/IP socket.  
        Socket listener = new Socket(ipAddress.AddressFamily,
            SocketType.Stream, ProtocolType.Tcp);
        listener.SetSocketOption(SocketOptionLevel.Socket, SocketOptionName.KeepAlive, true);

        try
        {
            listener.Bind(localEndPoint); // bind the socket to the local endpoint
            listener.Listen(10); // listen for incoming connections, queue up to 10 connections

            // main thread listens to new connections, hands incoming connections off to new threads  
            Log.Info("main thread listening...");
            while (true)
            {
                // waits for incoming connection
                Socket connection = listener.Accept();
                Thread thread = new Thread(() => handler(connection));
                thread.Start();
            }

        }
        catch (Exception e)
        {
            Log.Info($"server stopped unexpectedly: {e.ToString()}");
        }
        return 0;
    }

}

public class NotFoundException : Exception
{
    public NotFoundException(string message) : base(message)
    {
    }
}

public class ForbiddenException : Exception
{
    public ForbiddenException(string message) : base(message)
    {
    }
}

public class NotYetException : Exception
{
    public NotYetException(string message) : base(message)
    {
    }
}

public class GameState
{
    private static Mutex mutex = new Mutex();
    private static State state = new State();

    public static User CreateUser()
    {
        mutex.WaitOne();

        string username = UsernameGenerator.Next();
        while (state.Users.ContainsKey(username))
        {
            username = UsernameGenerator.Next();
        }
        var player = new User(username);
        state.Users.Add(username, player);

        mutex.ReleaseMutex();

        return player;
    }

    public static Game PairUser(string user)
    {
        Game? game = null;
        mutex.WaitOne();

        if (!userExists(user))
        {
            mutex.ReleaseMutex();
            throw new NotFoundException($"player with username {user} does not exist");
        }

        foreach (var (gameId, existingGame) in state.Games)
        {
            if (existingGame.Player1 == user || user == existingGame.Player2)
            {
                game = state.Games[gameId];
                state.Users[user].GameID = game.Id;
            }
            if (existingGame != null && existingGame.State == "waiting" && existingGame.Player1 != user)
            {
                state.Games[gameId].Player2 = user;
                state.Games[gameId].State = "progress";
                state.Users[user].GameID = gameId;
                game = state.Games[gameId];
                break;
            }
        }
        // NOTE: fallbacks to creating a game
        if (game == null)
        {
            game = new Game(System.Guid.NewGuid(), user);
            state.Games[game.Id] = game;
            state.Users[user].GameID = game.Id;
        }

        mutex.ReleaseMutex();

        return game;
    }

    public static User? Quit(string username, Guid gameId)
    {
        User? user = null;
        mutex.WaitOne();

        if (!userExists(username))
        {
            mutex.ReleaseMutex();
            throw new NotFoundException($"player with username {username} does not exist");
        }

        if (!gameExists(gameId))
        {
            mutex.ReleaseMutex();
            throw new NotFoundException($"player with username {username} does not exist");
        }

        var existingGameId = state.Users[username].GameID;
        if (existingGameId == null || existingGameId != gameId)
        {
            mutex.ReleaseMutex();
            throw new ForbiddenException($"player with username {username} not in game {gameId}");
        }

        state.Games.Remove(gameId);
        state.Users[username].GameID = null;
        user = state.Users[username];

        mutex.ReleaseMutex();
        return user;
    }

    public static string? GetOpponentMove(Guid gameId, string player)
    {
        mutex.WaitOne();

        if (!userExists(player))
        {
            mutex.ReleaseMutex();
            throw new NotFoundException($"player with username {player} does not exist");
        }

        if (!gameExists(gameId))
        {
            mutex.ReleaseMutex();
            throw new NotFoundException($"game with id {gameId} does not exist");
        }

        if (state.Users[player].GameID != gameId)
        {
            mutex.ReleaseMutex();
            throw new ForbiddenException($"player {player} not playing in game {gameId}");
        }

        if (state.Games[gameId].FirstPlayersTurn != (player == state.Games[gameId].Player1))
        {
            mutex.ReleaseMutex();
            throw new NotYetException($"other player has yet to make a move");
        }

        mutex.ReleaseMutex();
        return state.Games[gameId].LastMove;
    }

    public static Game MakeMove(Guid gameId, string player, string move)
    {
        mutex.WaitOne();

        if (!userExists(player))
        {
            mutex.ReleaseMutex();
            throw new NotFoundException($"player with username {player} does not exist");
        }

        if (!gameExists(gameId))
        {
            mutex.ReleaseMutex();
            throw new NotFoundException($"game with id {player} does not exist");
        }

        if (state.Users[player].GameID != gameId)
        {
            mutex.ReleaseMutex();
            throw new ForbiddenException($"player {player} not playing in game {gameId}");
        }

        var game = state.Games[gameId];
        if (state.Games[gameId].FirstPlayersTurn != (player == state.Games[gameId].Player1))
        {
            mutex.ReleaseMutex();
            throw new ForbiddenException($"it's not {player}'s turn");
        }

        state.Games[gameId].FirstPlayersTurn = !state.Games[gameId].FirstPlayersTurn;
        state.Games[gameId].LastMove = move;

        mutex.ReleaseMutex();
        return state.Games[gameId];
    }

    private static Game? findUsersGame(string username)
    {
        Game? game = null;

        var existingGameId = state.Users[username].GameID;
        if (existingGameId != null)
        {
            game = state.Games[existingGameId.Value];
        }

        return game;
    }

    private static bool userExists(string username)
    {
        return state.Users.ContainsKey(username);
    }

    private static bool gameExists(Guid game)
    {
        return state.Games.ContainsKey(game);
    }

    public static string JsonSnapshot()
    {
        return JsonSerializer.Serialize(state);
    }
}

// State represents the set of active players and current games
public class State
{
    [JsonPropertyName("games")]
    public Dictionary<Guid, Game> Games { get; set; }
    [JsonPropertyName("users")]
    public Dictionary<string, User> Users { get; set; }

    public State()
    {
        Games = new Dictionary<Guid, Game>();
        Users = new Dictionary<string, User>();
    }
}

// Player can be optionally associated to a game
public class User
{
    [JsonPropertyName("game_id")]
    public Guid? GameID { get; set; }
    [JsonPropertyName("name")]
    public string Name { get; set; }
    [JsonPropertyName("joined")]
    public DateTime Joined { get; set; }

    public User(string name)
    {
        Name = name;
        Joined = DateTime.Now;
    }
}

// Game has two players, first player initates the intent to play the game, second player just so happens
// to be active at the time. First player waits for second player. When second player shows intent to start a game, this
// instance of a game will begin.
public class Game
{
    [JsonPropertyName("id")]
    public Guid Id { get; set; }
    [JsonPropertyName("player_1")]
    public string Player1 { get; set; }
    [JsonPropertyName("player_2")]
    public string? Player2 { get; set; }
    [JsonPropertyName("first_players_turn")]
    public bool FirstPlayersTurn { get; set; }
    [JsonPropertyName("last_move")]
    public string? LastMove { get; set; }
    [JsonPropertyName("state")]
    public string State { get; set; } // TODO: enum?

    public Game(Guid id, string player1)
    {
        Id = id;
        Player1 = player1;
        FirstPlayersTurn = true;
        State = "waiting";
    }

    // IntentToPlayGame takes into account of a user's intent to play the game. User1 by virtue of creating the game
    // implicitly registers their intent to play a game. When user 2 also registers intent to play the game, the game state
    // becomes active.
    public void IntentToPlayGame(string player)
    {
        if (Player2 == player)
        {
            State = "progress";
        }
    }
}

public class UsernameGenerator
{
    public static string Next()
    {
        Random rnd = new Random();
        int randomNumber = rnd.Next(0, 100);
        return $"{KAnimals[rnd.Next(0, KAnimals.Length)]}_{randomNumber}";
    }

    // Yeah that's right, animals starting with the letter K only
    private static string[] KAnimals = {
            "Kai_Ken",
            "Kakapo",
            "Kangal",
            "Kangaroo",
            "Kangaroo_Rat",
            "Keel_Billed_Toucan",
            "Keelback",
            "Keeshond",
            "Kenyan_Sand_Boa",
            "Kerry_Blue_Terrier",
            "Kestrel",
            "Keta_Salmon",
            "Key_Deer",
            "Kiko_Goat",
            "Killdeer",
            "Killer_Whale",
            "Kinabalu_Giant_Red_Leech",
            "Kinder_Goat",
            "King_Cobra",
            "King_Crab",
            "King_Penguin",
            "King_Rat_Snake",
            "King_Shepherd",
            "King_Snake",
            "King_Vulture",
            "Kingfisher",
            "Kinkajou",
            "Kirtlands_snake",
            "Kishu",
            "Kit_Fox",
            "Kiwi",
            "Koala",
            "Kodkod",
            "Koi_Fish",
            "Komodo_Dragon",
            "Kooikerhondje",
            "Kookaburra",
            "Koolie",
            "Kori_Bustard",
            "Krill",
            "Kudu",
            "Kuvasz",
        };
}

// Request will host all utilities related to unmarshalling the request object, inspired by
// https://pkg.go.dev/net/http Request.
public class Request
{
    private byte[] Header;
    private byte[] Body;
    public string URL;

    public Request(byte[] body, byte[] header)
    {
        Header = header;
        Body = body;

        Match match = Regex.Match(Encoding.Default.GetString(Header), @"(?:GET|POST) (\/.+) HTTP");
        URL = match.Groups[1].Value;
    }

    public string Route()
    {
        if (URL == "")
        {
            return "/";
        }
        Match match = Regex.Match(URL, @"(\/[a-z]*)\??");
        return match.Groups.Count == 0 ? "/" : match.Groups[1].Value;
    }

    public System.Collections.Specialized.NameValueCollection Params()
    {
        if (URL == "")
        {
            return HttpUtility.ParseQueryString(URL);
        }
        Match match = Regex.Match(URL, @"(?:\/.*)[\?](.*)");
        return HttpUtility.ParseQueryString(match.Groups[1].Value);
    }
}

// ResponseWriter will host convenience around the connected socket with the client. Abstracting away from the response assembling
// inspired by https://pkg.go.dev/net/http ResponseWriter.
public class ResponseWriter
{
    private Socket Socket;

    public ResponseWriter(Socket connection)
    {
        Socket = connection;
    }

    public void Write(string jsonMarshalled, HttpStatusCode code)
    {
        string status = $"HTTP/1.1 {(int)code} {code.ToString()}\n";
        string header = "Content-Type: application/json\n";
        header += "Connection: Keep-Alive\n";
        header += "Access-Control-Allow-Origin: *\n";
        header += $"Content-Length: {Encoding.ASCII.GetBytes(jsonMarshalled).Length}\n";


        Socket.Send(Encoding.UTF8.GetBytes(status));
        Socket.Send(Encoding.UTF8.GetBytes(header));
        Socket.Send(Encoding.UTF8.GetBytes("\r\n"));
        Socket.Send(Encoding.UTF8.GetBytes(jsonMarshalled));
    }
}

// Log provides a standardised way of logging events
public class Log
{
    public static void Info(string logMessage)
    {
        var entry = new Dictionary<string, string>();
        entry.Add("time", DateTime.Now.ToString());
        entry.Add("message", logMessage);
        Console.WriteLine(JsonSerializer.Serialize(entry));
    }
}

// Util provides byte array searching utilities, in particular useful to find byte sequences
// in byte streams produced by clients to seperate request header and body.
static class HTTPRequestUtil
{
    // HTTP clients seperate headers and contents by a newline
    // we need to find Content-Length in order to know when to stop listening
    // from the stream of incoming bytes so we can hand off this payload to
    // a thread to work on
    public static byte[] ContentSeperator = new byte[] { 13, 10, 13, 10 };

    public static int ParseContentLength(byte[] raw)
    {
        string header = Encoding.Default.GetString(raw);
        string pattern = @"Content-Length: (\d+)";
        Match match = Regex.Match(header, pattern);
        if (match.Length == 0)
        {
            return 0;
        }
        return int.Parse(match.Groups[1].Value);
    }

    // Contains is a utility method that traverses the byte[] to find the searching
    // candidate, if found returns true with a populated point of reference representing
    // the index of the candidate
    public static bool Contains(this byte[] self, byte[] candidate, out int ep)
    {
        ep = 0;
        if (IsEmptyLocate(self, candidate))
            return false;

        for (int i = 0; i < self.Length; i++)
        {
            if (IsMatch(self, i, candidate))
            {
                ep = i;
                return true;
            }
        }

        return false;
    }

    static bool IsMatch(byte[] array, int position, byte[] candidate)
    {
        if (candidate.Length > (array.Length - position))
            return false;

        for (int i = 0; i < candidate.Length; i++)
            if (array[position + i] != candidate[i])
                return false;

        return true;
    }

    static bool IsEmptyLocate(byte[] array, byte[] candidate)
    {
        return array == null
                || candidate == null
                || array.Length == 0
                || candidate.Length == 0
                || candidate.Length > array.Length;
    }
}
