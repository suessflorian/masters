using System.Net;
using System.Text.Json;
using System.Security.Cryptography;
using System.Text;
using System.Reflection;

namespace Server
{
    class HttpServer
    {
        private static LogWriter logger = new LogWriter();
        private static MD5 md5 = MD5.Create();
        private static int WindowLength = 5;
        private static string staticpath = "./files/";
        private static List<HostedFile> hostedFiles = InitialiseHostedFiles(staticpath);
        private static string url = "http://localhost:8000/";

        private static void writeJsonResponse(HttpListenerResponse resp, string? serializedJson, HttpStatusCode code)
        {
            System.IO.Stream output = resp.OutputStream;
            if (serializedJson != null)
            {
                byte[] buffer = System.Text.Encoding.UTF8.GetBytes(serializedJson);
                resp.ContentLength64 = buffer.Length;
                resp.AddHeader("Content-Type", "application/json");
                output.Write(buffer, 0, buffer.Length);
            }
            resp.StatusCode = (int)code;
            output.Close();
        }

        private static void writeFile(HttpListenerResponse resp, byte[] buffer, string filename)
        {
            resp.ContentLength64 = buffer.Length;
            resp.AddHeader("Content-Disposition", "attachment");
            resp.AddHeader("filename", filename);
            resp.StatusCode = 200;
            System.IO.Stream output = resp.OutputStream;
            output.Write(buffer, 0, buffer.Length);
            output.Close();
        }

        private static void writeFragment(HttpListenerResponse resp, byte[] buffer)
        {
            resp.ContentLength64 = buffer.Length;
            resp.StatusCode = 200;
            System.IO.Stream output = resp.OutputStream;
            output.Write(buffer, 0, buffer.Length);
            output.Close();
        }

        private static void mux(HttpListenerRequest req, HttpListenerResponse resp)
        {
            string path = req.Url!.AbsolutePath;
            switch (path)
            {
                case "/files":
                    logger.Info("request received to list available files");
                    List<string> files = new List<string>();
                    foreach (HostedFile file in hostedFiles)
                        files.Add(file.Path.Substring(staticpath.Length));

                    writeJsonResponse(resp, JsonSerializer.Serialize(files), HttpStatusCode.OK);
                    return;
                default:
                    if (path.StartsWith("/download/"))
                    {
                        string requested = path.Substring("/download/".Length);
                        foreach (HostedFile file in hostedFiles)
                        {
                            if (requested == file.Path.Substring("./files/".Length))
                            {

                                logger.Info($"requested download of file {requested}");
                                writeFile(resp, File.ReadAllBytes(file.Path), requested);
                                return;
                            }
                        }
                        logger.Info($"requested download of non-existant file {requested}");
                        writeJsonResponse(resp, null, HttpStatusCode.NotFound);
                        return;
                    }
                    if (path.StartsWith("/fragments/"))
                    {
                        string requested = path.Substring("/fragments/".Length);
                        foreach (HostedFile file in hostedFiles)
                        {
                            if (requested == file.Path.Substring("./files/".Length))
                            {
                                List<string> fragments = new List<string>();
                                foreach (Fragment fragment in file.Fragments)
                                    fragments.Add(fragment.Fingerprint());

                                logger.Info($"requested fragments for {requested} file");
                                writeJsonResponse(resp, JsonSerializer.Serialize(fragments), HttpStatusCode.OK);
                                return;
                            }
                        }

                        logger.Info($"requested fragments of non-existant file {requested}");
                        writeJsonResponse(resp, null, HttpStatusCode.NotFound);
                        return;
                    }
                    if (path.StartsWith("/fragment/"))
                    {
                        string requested = path.Substring("/fragment/".Length);
                        foreach (HostedFile file in hostedFiles)
                        {
                            foreach (Fragment fragment in file.Fragments)
                            {
                                if (fragment.Fingerprint() == requested)
                                {

                                    logger.Info($"requested fragment {requested}");
                                    writeFragment(resp, fragment.Chunk);
                                    return;
                                }
                            }
                        }

                        logger.Info($"requested non-existant fragment {requested}");
                        writeJsonResponse(resp, null, HttpStatusCode.NotFound);
                        return;
                    }
                    // If mux matches nothing
                    writeJsonResponse(resp, null, HttpStatusCode.NotFound);
                    return;
            }

        }

        private static async Task serve(HttpListener listener)
        {
            while (true)
            {
                HttpListenerContext ctx = await listener.GetContextAsync(); // BLOCKING
                mux(ctx.Request, ctx.Response);
            }
        }

        // InitialiseHostedFiles returns a list of hosted files.
        // Each hosted file gets fragmented according to our implementation of a Rabing
        // function, we identifying fragment boundaries using a modded md5 function.
        private static List<HostedFile> InitialiseHostedFiles(string location)
        {
            logger.Info("initialising hosted files...");
            string[] staticfiles = Directory.GetFiles(location, "*", SearchOption.AllDirectories);

            List<HostedFile> hostedFiles = new List<HostedFile>();
            List<int> infoFragmentSizes = new List<int>();
            foreach (string file in staticfiles)
            {
                logger.Info($"found file {file}");
                byte[] stream = File.ReadAllBytes(file);
                HostedFile hosted = new HostedFile(file);
                List<byte> chunk = new List<byte>();

                for (int i = 0; i < stream.Length; i++)
                {
                    if (chunk.Count < WindowLength)
                    {
                        chunk.Add(stream[i]);
                        continue;
                    } // Fragments are at minimum the size of the window used as input for the Rabin function 
                    chunk.Add(stream[i]);
                    if (hitBoundary(chunk.GetRange(chunk.Count - WindowLength, WindowLength).ToArray()))
                    {
                        Fragment fragment = new Fragment(chunk, md5);
                        hosted.Fragments.Add(fragment);
                        infoFragmentSizes.Add(fragment.Chunk.Count());
                        chunk = new List<byte>();
                    }
                }
                if (chunk.Count > 0)
                {
                    Fragment fragment = new Fragment(chunk, md5);
                    hosted.Fragments.Add(new Fragment(chunk, md5));
                    infoFragmentSizes.Add(fragment.Chunk.Count());
                }


                logger.Info($"created {hosted.Fragments.Count()} fragments for file: {file}, average size: {(float)infoFragmentSizes.Sum() / (float)infoFragmentSizes.Count()}B");
                hostedFiles.Add(hosted);
                infoFragmentSizes = new List<int>();
            }

            logger.Info("finised fragmenting files");
            return hostedFiles;
        }

        private static bool hitBoundary(byte[] input)
        {
            return BitConverter.ToInt64(md5.ComputeHash(input), 0) % 2047 == 0; // ~2kB size fragments on average 
        }

        private static HttpListener listener = default!;
        public static void Main(string[] args)
        {
            logger.Info($"server listening on {url}");
            listener = new HttpListener();
            listener.Prefixes.Add(url);
            listener.Start();
            Task httpServer = serve(listener);
            httpServer.GetAwaiter().GetResult();

            logger.Info($"closing down server...");
            listener.Close();
        }
    }
}

public struct HostedFile
{
    public string Path;
    public List<Fragment> Fragments;

    public HostedFile(string path)
    {
        Fragments = new List<Fragment>();
        Path = path;
    }
}

public struct Fragment
{
    public byte[] Chunk;
    private MD5 md5;

    public Fragment(List<byte> chunk, MD5 md5)
    {
        Chunk = chunk.ToArray();
        this.md5 = md5;
    }

    public string Fingerprint()
    {
        var sBuilder = new StringBuilder();
        byte[] hash = md5.ComputeHash(Chunk);
        foreach (byte b in hash)
            sBuilder.Append(b.ToString("x2"));

        return sBuilder.ToString();
    }
}

public class LogWriter
{
    private string path = string.Empty;
    public LogWriter()
    {
        path = Path.Join(Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location) ?? ".", "log.txt");
        Console.WriteLine($"logger to write logs to {path}");
    }
    public void Info(string logMessage)
    {
        var entry = new Dictionary<string, string>();
        var time = DateTime.Now;
        entry.Add("time", time.ToString());
        entry.Add("message", logMessage);
        toConsole(JsonSerializer.Serialize(entry));
    }
    private void toConsole(string formattedMessage)
    {
        Console.WriteLine(formattedMessage);
    }
}
