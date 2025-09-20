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

                    case "reset":
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

                        string placeholder = cipher.GetCipher();

                        for (int i = 0; i < split; i++)
                        {
                            Console.WriteLine(cipher.IOC(split, i));
                            cipher.SetCipher(placeholder);
                        }
                        break;

                    case "check":
                        Console.Write("Phrase: ");
                        string phrase = Console.ReadLine();

                        Console.WriteLine(cipher.CheckPhrase(phrase));
                        break;

                    case "switch column":
                        Console.Write("Length of column: ");
                        int length = int.Parse(Console.ReadLine());

                        Console.Write("Index of column 1: ");
                        int col1 = int.Parse(Console.ReadLine());

                        Console.Write("Index of column 2: ");
                        int col2 = int.Parse(Console.ReadLine());

                        if (col1 <= length && col2 <= length)
                        {
                            cipher.SwitchColumns(length, col1 - 1, col2 - 1);
                        }
                        break;
                }

                cipher.PrintAlt();
                cipher.ResetTemp();
            }
        }
    }
}