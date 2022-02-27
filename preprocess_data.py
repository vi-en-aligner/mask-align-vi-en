import random
import os
import re

def read_from_file():
    vi_sents = []
    en_sents = []
    total_processed = 0
    f = open("data/data_gold_10000.txt", "r")
    for i, line in enumerate(f):
        if i % 3 == 0:
            total_processed += 1
        elif i % 3 == 1:
            vi_sents.append(line)
        elif i % 3 == 2:
            en_sents.append(line)

    assert total_processed == len(vi_sents) == len(en_sents)
    return total_processed, vi_sents, en_sents

def write_to_file(sents, file_name):
    with open(os.path.join("data/", file_name), "w") as writer:
        for sen in sents:
            writer.write(sen)


def process_en(sents):
    processed_sents = []
    for sen in sents:
        processed_sen = ' '.join([str.strip(s) for s in re.split("\(\{[ \d]*\}\)", sen)[1:]]) 
        processed_sents.append(processed_sen + '\n')
    
    return processed_sents

def create_ref(ref_sents):
    i = 0
    processed_refs = []
    for sen in ref_sents:
        refs = re.findall("\(\{[ \d]*\}\)", sen)
        pairs = []
        for i, ref in enumerate(refs):
            if i == 0:
                continue
            list_ref = list(map(int, ref[2:-2].split()))
            for p in list_ref:
                pairs.append(f'{p}-{i}')
        processed_refs.append(' '.join(pairs) + '\n')
    return processed_refs
    

if __name__ == '__main__':
    random.seed(9072000)
    total_processed, vi_sents, en_sents = read_from_file()
    ref_sents = en_sents
    en_sents = process_en(en_sents)
    
    train_len = int(total_processed * 0.8)
    # train_vi = vi_sents[:train_len]
    # train_en = en_sents[:train_len]
    test_vi = vi_sents[train_len:]
    test_en = en_sents[train_len:]
    test_ref_sents = ref_sents[train_len:]
    processed_refs = create_ref(test_ref_sents)

    # write_to_file(train_vi, "train_vi.src")
    # write_to_file(train_en, "train_en.tgt")
    write_to_file(test_vi, "test_vi.src")
    write_to_file(test_en, "test_en.tgt")
    write_to_file(processed_refs, "gold-vi-en.talp")
