using System.Net;
using System.Text.Json;
using System.Reflection;

namespace Client
{
    class HttpServer
    {
        private static LogWriter logger = new LogWriter();
        private static string url = "http://localhost:8002/";
        private static string server = "http://localhost:8001"; // NOTE: location of cache proxy
        private static readonly HttpClient client = new HttpClient();

        private static void writePage(HttpListenerResponse resp, string template)
        {
            System.IO.Stream output = resp.OutputStream;
            byte[] buffer = System.Text.Encoding.UTF8.GetBytes(template);
            resp.ContentLength64 = buffer.Length;
            output.Write(buffer, 0, buffer.Length);
            resp.StatusCode = 200;
            output.Close();
        }

        private static string wrapInTemplate(string body)
        {
            return @$"<!DOCTYPE html>
						<html>
							<title>Client</title>
							<meta name='description' content='Simple image viewing client'>
							<meta name='author' content='Florian Suess'>
						  <body>
								<div>
									<ul>
										<li><a href='/'>Home</a></li>
									</ul>
								</div>
								{body}
							</body>
						</html>";
        }

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

        private static async void mux(HttpListenerRequest req, HttpListenerResponse resp)
        {

            string path = req.Url!.AbsolutePath;
            switch (path)
            {
                case "/":
                    {
                        logger.Info("request received to list available files");
                        var res = await client.GetAsync(server + "/api/files");
                        if (res.StatusCode != HttpStatusCode.OK)
                        {
                            logger.Info("forwarding list available request failed");
                            writeJsonResponse(resp, JsonSerializer.Serialize($"got '{res.StatusCode.ToString()}' status code from server"), HttpStatusCode.InternalServerError);
                            return;
                        }
                        var files = JsonSerializer.Deserialize<string[]>(await res.Content.ReadAsStringAsync()) ?? new string[] { };

                        var template = "<ul>";
                        foreach (string file in files)
                            template += $"<li>{file} [<a href='{"/view/" + file}'>view</a>,<a href='{server + "/api/download/" + file}'>download</a>]</li>";

                        writePage(resp, wrapInTemplate(template + "</ul>"));
                        return;
                    }
                default:
                    if (path.StartsWith("/view/"))
                    {

                        var requestedImage = path.Substring("/view/".Length);
                        logger.Info($"request received to view file {requestedImage}");
                        switch (Path.GetExtension(requestedImage))
                        {
                            case ".jpg":
                            case ".jpeg":
                            case ".png":
                            case ".gif":
                                writePage(resp, wrapInTemplate($"<img src='{server + "/api/download/" + requestedImage}'/>"));
                                return;
                            case ".txt":
                                {
                                    var res = await client.GetAsync(server + "/api/download/" + requestedImage);
                                    if (res.StatusCode != HttpStatusCode.OK)
                                    {
                                        logger.Info($"failed to get image {requestedImage}");
                                        writeJsonResponse(resp, JsonSerializer.Serialize($"got '{res.StatusCode.ToString()}' status code from server"), HttpStatusCode.InternalServerError);
                                        return;
                                    }
                                    var body = await res.Content.ReadAsStringAsync();
                                    writePage(resp, wrapInTemplate($"<p>{body}</p>"));
                                    return;
                                }
                            case ".bmp":
                                {
                                    var res = await client.GetAsync(server + "/api/download/" + requestedImage);
                                    if (res.StatusCode != HttpStatusCode.OK)
                                    {
                                        logger.Info($"failed to get image {requestedImage}");
                                        writeJsonResponse(resp, JsonSerializer.Serialize($"got '{res.StatusCode.ToString()}' status code from server"), HttpStatusCode.InternalServerError);
                                        return;
                                    }
                                    var raw = await res.Content.ReadAsByteArrayAsync();
                                    writePage(resp, wrapInTemplate($"<img src='data:image/bmp;base64,{Convert.ToBase64String(raw)}'/>"));
                                    return;
                                }
                            default:
                                {
                                    writePage(resp, wrapInTemplate($"<p>file type not supported sorry, download should work fine though...</p>"));
                                    return;
                                }
                        }
                    }
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

        private static HttpListener listener = default!;
        public static void Main(string[] args)
        {
            logger.Info($"client listening on {url}");
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
