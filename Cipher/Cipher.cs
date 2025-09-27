using System;
using System.Collections.Generic;
using System.Diagnostics.Metrics;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;
using System.IO;

namespace cipher
{
    class Cipher
    {
        private string cipherText;
        private string altText;
        private string temp = "";

        public void InitCipher()
        {
            Console.Write("Enter cipher: ");
            cipherText = Console.ReadLine().ToUpper();
            altText = cipherText;
        }

        public void RemoveFiller()
        {
            for (int i = 0; i < altText.Length; i++)
            {
                int letter = (int)altText[i];

                if ((letter >= 65 && letter < 91) || (letter >= 97 && letter < 123))
                {
                    temp += (char)letter;
                }
            }

            altText = temp;
            ResetTemp();
        }

        public void AddFiller()
        {
            RemoveFiller();

            int setback = 0;
            for (int i = 0; i < cipherText.Length; i++)
            {
                int letter = (int)cipherText[i];

                if (letter < 65 || (letter >= 91 && letter < 97) || letter >= 123)
                {
                    temp += cipherText[i];
                    setback++;
                }

                else
                {
                    temp += altText[i - setback];
                }
            }

            altText = temp;
        }

        public void ReturnCipher()
        {
            altText = cipherText;
        }

        public void PrintAlt()
        {
            Console.WriteLine("\n" + altText);
        }

        public void ShiftManual()
        {
            Console.Write("Linear shift: ");
            int lShift = int.Parse(Console.ReadLine());

            Console.Write("Gap: ");
            int gap = int.Parse(Console.ReadLine());

            Console.Write("Offset: ");
            int offset = int.Parse(Console.ReadLine());

            Shift(lShift, gap, offset);
        }
        public void Shift(int linShift, int wordGap, int wordOffset)
        {
            RemoveFiller();

            if (wordGap <= 0)
            {
                wordGap = 1;
            }

            if (linShift < 0)
            {
                linShift = 0;
            }

            if (wordOffset < 0)
            {
                wordOffset = 0;
            }

            for (int i = 0; i < wordOffset; i++)
            {
                temp += altText[i];
            }

            for (int i = wordOffset; i < altText.Length; i += wordGap)
            {
                int ascii = (int)altText[i];

                if (ascii >= 65 && ascii < 91)
                {
                    temp += (char)((ascii - 65 + linShift) % 26 + 97);
                }

                else if (ascii >= 97 && ascii < 123)
                {
                    temp += (char)((ascii - 97 + linShift) % 26 + 97);
                }

                else
                {
                    temp += altText[i];
                }

                for (int j = 1; j < wordGap && i + j < altText.Length; j++)
                {
                    temp += altText[i + j];
                }
            }

            altText = temp;
            AddFiller();
        }

        public double IOC()
        {
            double repeat = 0;
            double total = 0;

            for (int i = 0; i < 26; i++)
            {
                int same = 0;

                foreach (char letter in cipherText)
                {
                    int ascii = letter;

                    if (ascii == 65 + i || ascii == 97 + i)
                    {
                        same++;
                    }
                }

                repeat += same * (same - 1);
            }

            if (repeat == 0)
            {
                return 0;
            }

            foreach (char letter in cipherText)
            {
                int ascii = letter;

                if (InABC(ascii))
                {
                    total++;
                }
            }

            total = total * (total - 1);

            return repeat / total;
        }

        public static bool InABC(int ascii)
        {
            return (ascii >= 65 && ascii < 91) || (ascii >= 97 && ascii < 123);
        }

        public static bool InABC(string text)
        {
            foreach (char letter in text)
            {
                int ascii = letter;
                if (!InABC(ascii))
                {
                    return false;
                }
            }

            return true;
        }

        public void Separate()
        {
            Console.Write("How much to separate by: ");
            int separate = int.Parse(Console.ReadLine());

            RemoveFiller();

            for (int i = 0; i < altText.Length; i += separate)
            {
                for (int j = 0; j < separate && i + j < altText.Length; j++)
                {
                    temp += altText[i + j];
                }

                temp += " ";
            }

            altText = temp;
        }

        public double IOC(int split, int offset)
        {

            for (int i = offset; i < altText.Length; i += split)
            {
                temp += altText[i];
            }

            cipherText = temp;
            temp = "";

            return IOC();
        }

        public string GetCipher()
        {
            return cipherText;
        }

        public void SetCipher(string text)
        {
            cipherText = text;
        }

        public int TotalLetters()
        {
            int total = 0;

            foreach (char letter in altText)
            {
                if (InABC(letter))
                {
                    total++;
                }
            }

            return total;
        }

        public int CheckPhrase(string phrase)
        {
            RemoveFiller();

            int total = 0;

            for (int i = 0; i < altText.Length; i++)
            {
                bool found = true;

                for (int j = 0; j < phrase.Length && i + j < altText.Length; j++)
                {
                    if (altText[i + j] != phrase[j])
                    {
                        found = false;
                    }
                }

                if (found)
                {
                    total++;
                }
            }

            AddFiller();
            return total;
        }

        public void ResetTemp()
        {
            temp = "";
        }

        public void SwitchColumns(int length, int col1, int col2)
        {
            RemoveFiller();

            for (int i = 0; i < altText.Length; i += length)
            {
                for (int j = 0; j < length && i + j < altText.Length; j++)
                {
                    if (j == col1)
                    {
                        temp += altText[i + col2];
                    }

                    else if (j == col2)
                    {
                        temp += altText[i + col1];
                    }

                    else
                    {
                        temp += altText[i + j];
                    }
                }
            }

            altText = temp;

            AddFiller();
        }

        public void Invert(int length)
        {
            RemoveFiller();

            for (int i = 0; i < length; i++)
            {
                for (int j = 0; i + j < altText.Length; j += length)
                {
                    temp += altText[i + j];
                }
                temp += " ";
            }

            altText = temp;
        }

        public void Tower(int length)
        {
            RemoveFiller();

            for (int i = 0; i < altText.Length; i += length)
            {
                for (int j = 0; j < length && i + j < altText.Length; j++)
                {
                    temp += altText[i + j];
                }

                temp += "\n";
            }

            altText = temp;
        }

        public void ReadFile()
        {
            cipherText = File.ReadAllText("Resources/cipher.txt").ToUpper();
            altText = cipherText;
        }

        public int FrequencyAnalysis(char chara)
        {
            int count = 0;

            foreach (char letter in altText)
            {
                if (letter == chara)
                {
                    count++;
                }
            }

            return Round((double)count * 100 / TotalLetters());
        }

        public int FrequencyAnalysis(int ascii)
        {
            char chara = (char)ascii;

            return FrequencyAnalysis(chara);
        }

        public static int Round(double num)
        {
            num += 0.5;

            return (int)num;
        }

        public int SelectiveFrequencyAnalysis(int length, int offset, int ascii)
        {
            RemoveFiller();
            temp = altText;
            altText = "";

            for (int i = offset; i < temp.Length; i += length)
            {
                altText += temp[i];
            }

            int frequency = FrequencyAnalysis(ascii);
            altText = temp;

            ResetTemp();
            AddFiller();
            ResetTemp();

            return frequency;
        }

        public void Substitute()
        {
            RemoveFiller();
            AddFiller();
            string swap;

            do
            {
                Console.Write("Letters to swap: ");
                swap = Console.ReadLine().ToLower();

                if (swap.Length == 2 && InABC(swap))
                {
                    ResetTemp();

                    foreach (char letter in altText)
                    {
                        int ascii = letter;
                        int identity = swap[0];

                        if (ascii + 32 == identity)
                        {
                            temp += swap[1];
                        }

                        else
                        {
                            temp += letter;
                        }
                    }

                    altText = temp;
                    Console.WriteLine($"\n{altText}\n");
                }
            } while (swap != "");
        }
    };
}