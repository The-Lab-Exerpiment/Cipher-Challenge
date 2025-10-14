from cipher_files import save_dict_to_file
from frequency_functions import get_tetragrams, index_of_coincidence, entropy
from generic_functions import strip_text


def format_corpus(file_name: str) -> str:
    lines = [str.upper(strip_text(k)) for k in open(file_name, "r").readlines()]
    return "".join(lines)


def train_tetragrams(file_name: str) -> dict:
    text = format_corpus(file_name)
    return get_tetragrams(text, decimal=False)


def get_ioc_example_data():
    for k in range(1, 6):
        a = index_of_coincidence(format_corpus("corpora/english_corpus_300k.txt"))
        b = index_of_coincidence(format_corpus("corpora/browncorpus"))
        c = index_of_coincidence(format_corpus("corpora/english_web.txt"))
        d = index_of_coincidence(format_corpus("corpora/world_at_war"))
        print(f"IOC{k}")
        print(f"English corpus (Wortschatz Leipzig) - News from 2005: {a}")
        print(f"Brown corpus: {b}")
        print(f"English corpus (Wortschatz Leipzig) - English web 2018: {c}")
        print(f"World at War: {d}")
        print(
            f"Cipher Challenge 1A + B (for reference) {
                index_of_coincidence(
                    strip_text('I will not distribute the answer on the interwebs')
                )
            }"
        )
        print(
            f"Pseudoradom text (for reference): {index_of_coincidence(format_corpus('random_text'), k)}"
        )
        print(
            f"Average (Not including Cipher Challenge Texts and Random) {(a + b + c + d) / 4}"
        )
        print()


def get_example_entropy_data():
    a = entropy(format_corpus("corpora/english_corpus_300k.txt"))
    b = entropy(format_corpus("corpora/browncorpus"))
    print("a")
    c = entropy(format_corpus("corpora/english_web.txt"))
    d = entropy(format_corpus("corpora/world_at_war"))
    print(f"Random text - {entropy(format_corpus('corpora/random_text'))}")
    print(f"English corpus (Wortschatz Leipzig) - News from 2005: {a}")
    print(f"Brown corpus : {b}")
    print(f"English corpus (Wortschatz Leipzig) - English web 2018: {c}")
    print(f"world_at_war: {d}")
    print(f"Average entropy of non-random texts: {(a + b + c + d) / 4}")


d = train_tetragrams(("corpora/english_corpus_300k.txt"))
print("d")
e = train_tetragrams(("corpora/browncorpus"))
print("e")
f = train_tetragrams(("corpora/english_web.txt"))
print("f")
g = train_tetragrams(("corpora/world_at_war"))
print("g")

for key in e:
    d[key] = d.get(key, 0) + e[key]
for key in f:
    d[key] = d.get(key, 0) + f[key]
for key in g:
    d[key] = d.get(key, 0) + g[key]

print(d)
save_dict_to_file(d, "new_tetragram_data.json")
