from typing import List, Dict, Any, Tuple
import string
import random


def n_partition(words: List[str], n_length: int) -> Dict[Tuple[str], List[str]]:
    """The function divides a given words list into different 
       partitions of length n_length. Each partition will be set as a
       key from a dict wich maps to the word in the words list at 
       the following index position n_length + 1.

       Since same word partitions may be followed by different words, 
       all the possible following words will be stored in a list.
       This list collection with multiple following words is set as
       value to the partition key in the dict.

    Arguments:  
        words {List[]str} -- words from a given text are stored in a list, 
                             ordered by occurence within the text
        n_length {int}    -- length of the partition keys

    Returns:
        Dict[Tuple[str], List[str]] -- Dict mapping from partitions to 
                                       valid next words
    """
    part_dict = dict()
    for index, word in enumerate(words):
        try:
            # get next partition with length n_length as dict key
            partition_key = tuple(words[index + j] for j in range(n_length))
            value = part_dict.setdefault(partition_key, [])
            # map the next word to the partition_key which is not contained
            # in the partition key itself as element
            value.append(words[index + n_length])
        except IndexError:
            continue
    return part_dict


def random_step(
    part_key: Tuple[str], partitions: Dict[Tuple[str], List[str]]
) -> List[str]:
    """Choose randomly from the next valid words. 

    Arguments:
        part_key {Tuple} -- key in partitions
        partitions {List[Tuple]} -- dictionary with possible next 
                                    steps for a key

    Returns:
        {List} -- next word, randomly chosen from a given set of 
                  valid answers
    """
    next_walk = partitions.get(part_key, [])
    # choose randomly only if there are two choices at least
    if len(next_walk) > 1:
        next_walk = [random.choice(next_walk)]
    return part_key[1:] + tuple(next_walk), next_walk


def random_walk(
    init_partition: Tuple[str], partitions: Dict[Tuple[str], List[str]]
) -> List[List[str]]:
    """Perform a random walk, according to a given partitions dict 
       which maps from a given set of partitions to a valid set
       of possible next words. Within this set it will be choosen 
       randomly. 

    Arguments:
        init_partition {Tuple[str]} -- initial key to start the random walk
        partitions {Dict[Tuple[str], List[str]]} -- random walk map with 
                                                    possible choices

    Returns:
        List[List[str]] -- Randomly choosen words, gained through a
                           random walk
    """
    # modify structure of initial input to match the output structure
    walk_list = [word for word in init_partition]
    iter_tuple = init_partition
    next_word = [""]
    while next_word != []:
        iter_tuple, next_word = random_step(iter_tuple, partitions)
        # unpack List[str] to append only strings, except the empty list
        # which causes an IndexError
        try:
            walk_list.append(next_word[0])
        except IndexError:
            continue
    return walk_list


def read_file(filename):
    words = []
    with open(filename, "r") as file:
        for line in file:
            line = line.replace("-", " ")
            for word in line.split():
                word = word.strip(string.punctuation + string.whitespace)
                word = word.lower()
                words.append(word)
    return words


def main():
    # store words in list
    # TODO: imporove text preprocessing
    # words = read_file("test_text.txt")
    words = read_file("hudson.txt")

    # transform words in partitions which will serves as
    # keys for a random walk
    n_length = 2
    partitions = n_partition(words, n_length)

    # choose an initial partition for the random walk
    init_part = random.choice(list(partitions.keys()))
    walk_list = random_walk(init_part, partitions)

    random_walk_text = " ".join(walk_list)

    print(random_walk_text)


if __name__ == "__main__":
    main()
