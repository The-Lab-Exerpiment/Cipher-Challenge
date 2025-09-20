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
                        cipher.InitCipher();
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

                    case "split":
                        cipher.Separate();
                        break;

                    case "ioc split":
                        Console.Write("Separation: ");
                        int split = int.Parse(Console.ReadLine());

                        string temp = cipher.GetCipher();

                        for (int i = 0; i < split; i++)
                        {
                            Console.WriteLine(cipher.IOC(split, i));
                        }

                        cipher.SetCipher(temp);
                        break;
                }

                cipher.PrintAlt();
            }
        }
    }
}