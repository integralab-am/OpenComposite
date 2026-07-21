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
            await Task.Delay(1);
            return null;
        }
    }
}
