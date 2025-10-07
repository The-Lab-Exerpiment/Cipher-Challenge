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
        private int[,,,] tetragrams = new int[26, 26, 26, 26];

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

        public string FindKey(int split)
        {
            RemoveFiller();
            string tempAlt = altText;

            double[] englishFrequency = { 8.04, 1.53, 3.11, 3.96, 12.50, 2.34, 1.95, 5.41, 7.3, 0.16, 0.66, 4.13, 2.15, 7.10, 7.60, 2.02, 0.11, 6.14, 6.55, 9.25, 2.71, 1.00, 1.88, 0.10, 1.72, 0.10 };

            string key = "";

            for (int i = 0; i < split; i++)
            {
                altText = "";

                for (int j = i; j < tempAlt.Length; j += split)
                {
                    altText += tempAlt[j];
                }

                char letter = ' ';
                double max = 0;

                for (int shift = 0; shift < 26; shift++)
                {
                    Shift(1, 1, 0);

                    double[] frequency = new double[26];

                    for (int j = 0; j < 26; j++)
                    {
                        frequency[j] = FrequencyAnalysis(65 + j) + FrequencyAnalysis(97 + j);
                    }

                    double rank = DotProduct(frequency, englishFrequency, 26);

                    if (rank > max)
                    {
                        letter = (char)('z' - shift);
                        max = rank;
                    }

                    ResetTemp();
                }

                key += letter;
            }

            altText = tempAlt;
            AddFiller();

            return key;
        }

        public double DotProduct(double[] vector1, double[] vector2, int length)
        {
            double total = 0;

            for (int i = 0; i < length; i++)
            {
                total += vector1[i] * vector2[i];
            }

            return total;
        }

        public void KeyWordShift(string key)
        {
            if (InABC(key))
            {
                for (int i = 0; i < key.Length; i++)
                {
                    Shift('Z' - key[i] + 1, key.Length, i);
                    ResetTemp();
                }
            }

            AddFiller();
        }

        public string RemoveFiller(string text)
        {
            string ogAltText = altText;
            altText = text;

            RemoveFiller();
            text = altText;
            altText = ogAltText;

            return text;
        }

        public void ResetTetragrams()
        {
            for (int i3 = 0; i3 < 26; i3++)
            {
                for (int i2 = 0; i2 < 26; i2++)
                {
                    for (int i1 = 0; i1 < 26; i1++)
                    {
                        for (int i0 = 0; i0 < 26; i0++)
                        {
                            tetragrams[i3, i2, i1, i0] = 0;
                        }
                    }
                }
            }
        }

        public void TrainTetragrams(string filePath)
        {
            string train = RemoveFiller(File.ReadAllText(filePath)).ToUpper();
            ResetTetragrams();

            for (int i = 0; i < train.Length - 3; i++)
            {
                tetragrams[train[i] - 65, train[i + 1] - 65, train[i + 2] - 65, train[i + 3] - 65]++;
            }
        }

        public int Tetragram(string tetragram)
        {
            tetragram = tetragram.ToUpper();

            if (tetragram.Length == 4 && InABC(tetragram))
            {
                return tetragrams[tetragram[0] - 65, tetragram[1] - 65, tetragram[2] - 65, tetragram[3] - 65];
            }

            return -1;
        }

        public void SaveTetragrams(string filePath)
        {
            for (int i3 = 0; i3 < 26; i3++)
            {
                for (int i2 = 0; i2 < 26; i2++)
                {
                    for (int i1 = 0; i1 < 26; i1++)
                    {
                        for (int i0 = 0; i0 < 26; i0++)
                        {
                            temp += tetragrams[i3, i2, i1, i0].ToString() + "\n";
                        }
                    }
                }
            }

            File.WriteAllText(filePath, temp);
        }

        public void ReadTetragrams(string filePath)
        {
            temp = File.ReadAllText(filePath);
            string num = "";
            int count = 0;

            foreach (char letter in temp)
            {
                if (letter == '\n')
                {
                    tetragrams[(count / (26 * 26 * 26)) % 26, (count / (26 * 26)) % 26, (count / 26) % 26, count % 26] = int.Parse(num);
                    num = "";
                    count++;
                }

                else
                {
                    num += letter;
                }
            }

            ResetTemp();
        }

        public string FitnessKey(int length)
        {
            string ogAltText = altText;

            double fitness = double.MinValue;

            string tempKey = "";

            for (int i = 0; i < length; i++)
            {
                tempKey += "A";
            }

            string key;

            do
            {
                key = tempKey;
                KeyWordShift(key);
                ResetTemp();

                tempKey = "";

                for (int i = 0; i < length; i++)
                {
                    char best = key[i];

                    for (int shift = 0; shift < 26; shift++)
                    {
                        if (Fitness() > fitness)
                        {
                            fitness = Fitness();
                            best = (char)((key[i] + -'A' + shift) % 26 + 'A');
                        }

                        Shift(1, length, i);
                        ResetTemp();
                    }

                    tempKey += best;

                    altText = ogAltText;
                    string newKey = tempKey;

                    for (int j = i + 1; j < length; j++)
                    {
                        newKey += key[j];
                    }

                    KeyWordShift(newKey);
                }

                altText = ogAltText;

            } while (key != tempKey);

            return key;
        }

        public int CountTetragram(string tetragram)
        {
            int count = 0;

            if (tetragram.Length == 4 && InABC(tetragram))
            {
                tetragram = tetragram.ToUpper();
                RemoveFiller();
                altText = altText.ToUpper();

                for (int i = 0; i < altText.Length - 3; i++)
                {
                    if (tetragram[0] == altText[i] && tetragram[1] == altText[i + 1] && tetragram[2] == altText[i + 2] && tetragram[3] == altText[i + 3])
                    {
                        count++;
                    }
                }

                AddFiller();
            }

            return count;
        }

        public int CountTetragram(int i1, int i2, int i3, int i4)
        {
            int count = 0;

            for (int i = 0; i < altText.Length - 3; i++)
            {
                if (i1 + 65 == altText[i] && i2 + 65 == altText[i + 1] && i3 + 65 == altText[i + 2] && i4 + 65 == altText[i + 3])
                {
                    count++;
                }
            }

            return count;
        }

        public double Fitness()
        {
            double fitness = 0;

            for (int i1 = 0; i1 < 26; i1++)
            {
                for (int i2 = 0; i2 < 26; i2++)
                {
                    for (int i3 = 0; i3 < 26; i3++)
                    {
                        for (int i4 = 0; i4 < 26; i4++)
                        {
                            fitness += Math.Log(CountTetragram(i1, i2, i3, i4));
                        }
                    }
                }
            }

            return fitness;
        }
    };
}