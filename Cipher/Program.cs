using System.Runtime.InteropServices;

namespace cipher
{
    internal class Program
    {
        static void Main(string[] args)
        {
            Cipher cipher = new Cipher();
            cipher.ReadTetragrams("Data/tetragrams.txt");

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
                        cipher.AddFiller();
                        break;

                    case "ioc":
                        Console.WriteLine($"{cipher.IOC() * 100}%");
                        break;

                    case "split":
                        cipher.Separate();
                        break;

                    case "iocs":
                        Console.Write("Separation: ");
                        int split = int.Parse(Console.ReadLine());

                        string placeholder = cipher.GetCipher();
                        cipher.RemoveFiller();

                        for (int i = 0; i < split; i++)
                        {
                            Console.WriteLine($"{i + 1}/{split} : {cipher.IOC(split, i) * 100}%");
                            cipher.SetCipher(placeholder);
                        }

                        cipher.AddFiller();
                        break;

                    case "check":
                        Console.Write("Phrase: ");
                        string phrase = Console.ReadLine();

                        Console.WriteLine(cipher.CheckPhrase(phrase));
                        break;

                    case "switch":
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

                    case "invert":
                        Console.Write("Length of row: ");
                        length = int.Parse(Console.ReadLine());
                        cipher.Invert(length);
                        break;

                    case "stack":
                        Console.Write("Length of row: ");
                        length = int.Parse(Console.ReadLine());
                        cipher.Tower(length);
                        break;

                    case "og":
                        Console.WriteLine(cipher.GetCipher());
                        break;

                    case "read":
                        cipher.ReadFile();
                        break;

                    case "analyse":
                        cipher.RemoveFiller();
                        for (int i = 0; i < 26; i++)
                        {
                            Console.WriteLine($"{(char)(65 + i)}: {cipher.FrequencyAnalysis(65 + i) + cipher.FrequencyAnalysis(97 + i)}%");
                        }
                        cipher.AddFiller();
                        break;
                    case "select":
                        Console.Write("Length of row: ");
                        length = int.Parse(Console.ReadLine());

                        Console.Write("Offset: ");
                        int offset = int.Parse(Console.ReadLine());


                        for (int i = 0; i < 26; i++)
                        {
                            Console.WriteLine($"{(char)(65 + i)}: {cipher.SelectiveFrequencyAnalysis(length, offset, 65 + i) + cipher.SelectiveFrequencyAnalysis(length, offset, 97 + i)}%");
                        }
                        break;

                    case "cshift":
                        Console.Write("Amount of shift: ");
                        int shift = int.Parse(Console.ReadLine());

                        cipher.Shift(shift, 1, 0);
                        cipher.AddFiller();
                        break;

                    case "sub":
                        cipher.Substitute();
                        break;

                    case "key":
                        Console.Write("Length of row: ");
                        length = int.Parse(Console.ReadLine());

                        Console.WriteLine($"Possible key: {cipher.FindKey(length)}");
                        break;

                    case "kshift":
                        Console.Write("Enter key: ");
                        string key = Console.ReadLine().ToUpper();

                        cipher.KeyWordShift(key);
                        break;

                    case "train":
                        cipher.TrainTetragrams("Resources/train.txt");
                        break;

                    case "get tetragram":  // dev tool, remove once testing is over
                        Console.Write("Enter tetragram: ");
                        string tetra = Console.ReadLine();
                        Console.WriteLine(cipher.Tetragram(tetra).ToString());
                        break;

                    case "save":
                        cipher.SaveTetragrams("Data/tetragrams.txt");
                        break;
                }

                cipher.PrintAlt();
                cipher.ResetTemp();
            }
        }
    }
}