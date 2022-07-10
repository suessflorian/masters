using System.Net;
using System.Text.Json;
using System.Text;
using System.Reflection;

namespace Server
{
    class HttpServer
    {
        private static LogWriter logger = new LogWriter();
        private static Dictionary<string, byte[]> cache = new Dictionary<string, byte[]>();
        private static string url = "http://localhost:8001/";
        private static string server = "http://localhost:8000";
        private static readonly HttpClient client = new HttpClient();

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
							<title>Proxy Cache Server</title>
							<meta name='description' content='GUI for interacting with the proxy cache server'>
							<meta name='author' content='Florian Suess'>
						  <body>
								<div>
									<ul>
										<li><a href='/'>Home</a></li>
										<li><a href='/logs'>Logs</a></li>
										<li><a href='/api/purge-cache'>Clear Cache</a></li>
										<li><a href='/api/purge-logs'>Clear Logs</a></li>
									</ul>
								</div>
								{body}
							</body>
						</html>";
        }

        private static async void mux(HttpListenerRequest req, HttpListenerResponse resp)
        {
            string path = req.Url!.AbsolutePath;
            switch (path)
            {
                case "/":
                    {
                        var fragments = "<ul>";
                        foreach (var fragment in cache.Keys)
                            fragments += $"<li>{fragment} [<a href='/fragment/{fragment}'>view</a>]</li>";
                        writePage(resp, wrapInTemplate(fragments + "</ul>"));
                        return;
                    }

                case "/logs":
                    writePage(resp, wrapInTemplate($"<p style='white-space: pre-line'>{logger.Dump()}</p>"));
                    return;

                case "/api/files":
                    {
                        logger.Info("request received to list available files");
                        var res = await client.GetAsync(server + "/files");
                        if (res.StatusCode != HttpStatusCode.OK)
                        {
                            logger.Info("forwarding list available request failed");
                            writeJsonResponse(resp, JsonSerializer.Serialize($"got '{res.StatusCode.ToString()}' status code from server"), HttpStatusCode.InternalServerError);
                            return;
                        }
                        var body = await res.Content.ReadAsStringAsync(); // assumes JSON response
                        logger.Info("successfully forwarded request to list files");
                        writeJsonResponse(resp, body, HttpStatusCode.OK);
                        return;
                    }
                case "/api/purge-cache":
                    logger.Info("request to purge cache");
                    cache = new Dictionary<string, byte[]>();
                    logger.Info("successfully purged cache... redirecting to /");
                    resp.Redirect(url);
                    resp.Close();
                    return;
                case "/api/purge-logs":
                    logger.Info("request to purge logs");
                    logger.Purge();
                    logger.Info("successfully purged logs... redirecting to /");
                    resp.Redirect(url);
                    resp.Close();
                    return;
                default:
                    if (path.StartsWith("/fragment/"))
                    {
                        var requestedFragment = path.Substring("/fragment/".Length);
                        if (!cache.ContainsKey(requestedFragment))
                        {
                            writeJsonResponse(resp, null, HttpStatusCode.NotFound);
                            return;
                        }
                        logger.Info($"request to view fragment {requestedFragment}");
                        var fragment = cache[requestedFragment]; // assumes existant fragment, TODO: handle 404 for nicety
                        writePage(resp, wrapInTemplate($"<p style='word-wrap: break-word'>{toHexadecimalRepresentation(fragment)}</p>"));
                        return;
                    }
                    if (path.StartsWith("/api/download/"))
                    {
                        var requestedFile = path.Substring("/api/download/".Length);
                        logger.Info($"received request for {requestedFile} file");
                        var res = await client.GetAsync(server + "/fragments/" + requestedFile);
                        if (res.StatusCode == HttpStatusCode.NotFound)
                        {
                            logger.Info($"requested download of file {requestedFile} is deemed non-existant by server");
                            writeJsonResponse(resp, null, HttpStatusCode.NotFound);
                            return;
                        }
                        if (res.StatusCode != HttpStatusCode.OK)
                        {
                            logger.Info($"failed to request list of fragments for file {requestedFile}");
                            writeJsonResponse(resp, JsonSerializer.Serialize($"got '{res.StatusCode.ToString()}' status code from server"), HttpStatusCode.InternalServerError);
                            return;
                        }
                        var body = await res.Content.ReadAsStringAsync();
                        var fingerprints = JsonSerializer.Deserialize<string[]>(body);
                        if (fingerprints == null || fingerprints.Length < 1)
                        {
                            logger.Info($"unexpected empty list of fragments for file {requestedFile}");
                            writeJsonResponse(resp, JsonSerializer.Serialize("got unexpected fingerprint response from server"), HttpStatusCode.InternalServerError);
                            return;
                        }

                        HashSet<string> fragmentsLeftToFetch = new HashSet<string>();
                        foreach (string fingerprint in fingerprints)
                            if (!cache.ContainsKey(fingerprint))
                                fragmentsLeftToFetch.Add(fingerprint);

                        foreach (string fragment in fragmentsLeftToFetch)
                        {
                            try
                            {
                                res = await client.GetAsync(server + "/fragment/" + fragment);
                                if (res.StatusCode != HttpStatusCode.OK)
                                    throw new Exception();
                                var bytes = await res.Content.ReadAsByteArrayAsync();
                                cache.Add(fragment, bytes);
                                logger.Info($"cached fragment with fingerprint {fragment}");
                            }
                            catch
                            {
                                logger.Info($"failed to fetch and cache fragment {fragment}");
                                writeJsonResponse(resp, null, HttpStatusCode.InternalServerError);
                                return;
                            }
                        }

                        List<byte[]> fragments = new List<byte[]>();
                        foreach (string fingerprint in fingerprints)
                        {
                            fragments.Add(cache[fingerprint]);
                        }

                        logger.Info($"%{100 - ((float)fragmentsLeftToFetch.Count() / (float)fingerprints.Count()) * 100} of file {requestedFile} constructed with cached data");
                        writeFile(resp, combineFragments(fragments.ToArray()), requestedFile);
                        return;
                    }

                    // If mux matches nothing
                    writeJsonResponse(resp, null, HttpStatusCode.NotFound);
                    return;
            }
        }
        private static byte[] combineFragments(params byte[][] arrays)
        {
            byte[] rv = new byte[arrays.Sum(a => a.Length)];
            int offset = 0;
            foreach (byte[] array in arrays)
            {
                System.Buffer.BlockCopy(array, 0, rv, offset, array.Length);
                offset += array.Length;
            }
            return rv;
        }

        private static string toHexadecimalRepresentation(byte[] bytes)
        {
            StringBuilder hex = new StringBuilder(bytes.Length * 2);
            foreach (byte b in bytes)
                hex.AppendFormat("{0:x2}", b);
            return hex.ToString();
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
            logger.Info($"proxy listening on {url}");
            listener = new HttpListener();
            listener.Prefixes.Add(url);
            listener.Start();
            Task httpServer = serve(listener);
            httpServer.GetAwaiter().GetResult();

            logger.Info($"closing down server");
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
        Info($"logger to write logs to {path}");
    }
    public string Dump()
    {
        return File.ReadAllText(path);
    }
    public void Purge()
    {
        File.WriteAllText(path, string.Empty);
    }
    public void Info(string logMessage)
    {
        var entry = new Dictionary<string, string>();
        var time = DateTime.Now;
        entry.Add("time", time.ToString());
        entry.Add("message", logMessage);
        toFile(JsonSerializer.Serialize(entry));
        toConsole(JsonSerializer.Serialize(entry));
    }

    private void toFile(string formattedMessage)
    {
        using (StreamWriter w = File.AppendText(path))
            w.Write($"{formattedMessage}\r\n");
    }
    private void toConsole(string formattedMessage)
    {
        Console.WriteLine(formattedMessage);
    }
}
