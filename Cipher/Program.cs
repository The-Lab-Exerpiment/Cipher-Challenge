using System.Runtime.InteropServices;

namespace cipher
{
    internal class Program
    {
        static void Main(string[] args)
        {
            Cipher cipher = new Cipher();

            while (true)
            {
                Console.Write("\nWhat is your command? ");

                switch (Console.ReadLine().ToLower())
                {
                    case "enter":
                        cipher.GetCipher();
                        break;
                    case "remove":
                        cipher.RemoveFiller();
                        break;
                    case "add":
                        cipher.AddFiller();
                        break;
                    case "return":
                        cipher.ReturnCipher();
                        break;
                    case "shift":
                        cipher.ShiftManual();
                        break;
                    case "ioc":
                        Console.WriteLine(cipher.IOC());
                        break;
                }

                cipher.PrintAlt();
            }
        }
    }
}