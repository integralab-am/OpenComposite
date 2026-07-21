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
        class GitHubCommitInfo
        {
            public string sha;
        }

        private static string sha;

        public static async Task<string> GetLatestHash()
        {
            if (sha != null)
                return sha;

            try {
                ServicePointManager.SecurityProtocol |= SecurityProtocolType.Tls12;
                using (WebClient wc = new WebClient())
                {
                    wc.Headers.Add("User-Agent", "OpenComposite-RuntimeSwitcher");
                    string json = await wc.DownloadStringTaskAsync("https://api.github.com/repos/integralab-am/OpenComposite/commits/openxr");
                    
                    GitHubCommitInfo commit = JsonConvert.DeserializeObject<GitHubCommitInfo>(json);
                    return sha = commit.sha;
                }
            } catch {
                return null;
            }
        }
    }
}
