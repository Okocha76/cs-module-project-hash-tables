def word_count(s):
    word_count = {}
    ignore_chars = '" : ; , . - + = / \ | [ ] { } ( ) * ^ &'
    words = s.split()
    for word in words:
        for char in ignore_chars:
            if char in word:
                word = word.replace(char,'')
        word = word.lower()
        if word:
            if not word in word_count:
                word_count[word] = 1
            else:
                word_count[word] += 1
    return word_count


if __name__ == "__main__":
    print(word_count(""))
    print(word_count("Hello"))
    print(word_count('Hello, my cat. And my cat doesn\'t say "hello" back.'))
    print(word_count('This is a test of the emergency broadcast network. This is only a test.'))