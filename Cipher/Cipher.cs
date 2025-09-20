using System;
using System.Collections.Generic;
using System.Diagnostics.Metrics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace cipher
{
    class Cipher
    {
        private string cipherText;
        private string altText;

        public void GetCipher()
        {
            Console.Write("Enter cipher: ");
            cipherText = Console.ReadLine().ToUpper();
            altText = cipherText;
        }

        public void RemoveFiller()
        {
            string temp = "";

            for (int i = 0; i < altText.Length; i++)
            {
                int letter = (int)altText[i];

                if ((letter >= 65 && letter < 91) || (letter >= 97 && letter < 123))
                {
                    temp += (char)letter;
                }
            }

            altText = temp;
        }

        public void AddFiller()
        {
            int setback = 0;
            string temp = "";

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
            Console.Write("Geometric shift: ");
            int gShift = int.Parse(Console.ReadLine());

            Console.Write("Linear shift: ");
            int lShift = int.Parse(Console.ReadLine());

            Console.Write("Gap: ");
            int gap = int.Parse(Console.ReadLine());

            Console.Write("Offset: ");
            int offset = int.Parse(Console.ReadLine());

            Shift(gShift, lShift, gap, offset);
        }
        private void Shift(int geoShift, int linShift, int wordGap, int wordOffset)
        {
            string temp = "";
            RemoveFiller();

            if (wordGap <= 0)
            {
                wordGap = 1;
            }

            if (geoShift <= 0)
            {
                geoShift = 1;
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
                    temp += (char)(((ascii - 65) * geoShift + linShift) % 26 + 97);
                }

                else if (ascii >= 97 && ascii < 123)
                {
                    temp += (char)(((ascii - 97) * geoShift + linShift) % 26 + 97);
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
    };
}