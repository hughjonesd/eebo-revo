# must work in both .sh and .python
# in sh: "source ./configsh.py"
# note the ./ is necessary for sbatch to be happy
# in py: "import configsh"
# format: name=value

FASTTEXT_DIMS=750
TEI_FILES_PATH="data/TEI-files.tab"
SIMILAR_WORDS_PATH="data/similar-words.tab"
LEME_SCRATCH_DIR="data/leme-cleaned"
