using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;

namespace RuntimeSwitcher
{
    class UpdateChecker
    {
        class Commit
        {
            public string id;
        }

        private static string id;

        public static async Task<string> GetLatestHash()
        {
            if (id != null)
                return id;

            try {
                ServicePointManager.SecurityProtocol |= SecurityProtocolType.Tls12;
                using (WebClient wc = new WebClient())
                {
                    wc.Headers.Add("User-Agent", "OpenComposite-RuntimeSwitcher");
                    string json = await wc.DownloadStringTaskAsync("https://gitlab.com/api/v4/projects/znixian%2fOpenOVR/repository/commits/openxr?per_page=1");

                    if (json.Substring(0, 1) != "[")
                        json = "[" + json + "]";
                    
                    Commit commit = JsonConvert.DeserializeObject<List<Commit>>(json).First();

                    return id = commit.id;
                }
            } catch {
                return null;
            }
        }
    }
}
