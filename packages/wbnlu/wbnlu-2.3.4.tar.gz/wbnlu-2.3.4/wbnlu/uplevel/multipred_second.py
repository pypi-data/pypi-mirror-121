# coding=utf-8
"""BERT finetuning runner of classification for online prediction. input is a list. output is a label."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

os.environ["CUDA_VISIBLE_DEVICES"] = "1"

import collections
import csv
import os
import modeling
import optimization
import tokenization
import tensorflow as tf
import numpy as np
import datetime
flags = tf.flags

FLAGS = flags.FLAGS

## Required parameters
BERT_BASE_DIR="/data6/maohui/workspace/bert_base_dir/chinese_L-12_H-768_A-12/"
#flags.DEFINE_string("bert_config_file", BERT_BASE_DIR+"bert_config.json",
flags.DEFINE_string("bert_config_file", BERT_BASE_DIR+"bert_config_4layer.json",
    "The config json file corresponding to the pre-trained BERT model. "
    "This specifies the model architecture.")

flags.DEFINE_string("task_name", "weibo", "The name of the task to train.")

flags.DEFINE_string("vocab_file", BERT_BASE_DIR+"vocab.txt",
                    "The vocabulary file that the BERT model was trained on.")

#flags.DEFINE_string("init_checkpoint", "/data6/maohui/workspace/model_output/second_ml/", 
flags.DEFINE_string("init_checkpoint", "/data6/maohui/workspace/model_output/second_ml_4layer/", 
    "Initial checkpoint (usually from a pre-trained BERT model).")

flags.DEFINE_integer("max_seq_length", 256,
    "The maximum total input sequence length after WordPiece tokenization. "
    "Sequences longer than this will be truncated, and sequences shorter "
    "than this will be padded.")

flags.DEFINE_bool(
    "do_lower_case", True,
    "Whether to lower case the input text. Should be True for uncased "
    "models and False for cased models.")

class InputExample(object):
  """A single training/test example for simple sequence classification."""

  def __init__(self, guid, text_a, text_b=None, label=None):
    """Constructs a InputExample.

    Args:
      guid: Unique id for the example.
      text_a: string. The untokenized text of the first sequence. For single
        sequence tasks, only this sequence must be specified.
      text_b: (Optional) string. The untokenized text of the second sequence.
        Only must be specified for sequence pair tasks.
      label: (Optional) string. The label of the example. This should be
        specified for train and dev examples, but not for test examples.
    """
    self.guid = guid
    self.text_a = text_a
    self.text_b = text_b
    self.label = label


class InputFeatures(object):
  """A single set of features of data."""

  def __init__(self, input_ids, input_mask, segment_ids, label_id):
    self.input_ids = input_ids
    self.input_mask = input_mask
    self.segment_ids = segment_ids
    self.label_id = label_id


class DataProcessor(object):
  """Base class for data converters for sequence classification data sets."""

  def get_train_examples(self, data_dir):
    """Gets a collection of `InputExample`s for the train set."""
    raise NotImplementedError()

  def get_dev_examples(self, data_dir):
    """Gets a collection of `InputExample`s for the dev set."""
    raise NotImplementedError()

  def get_test_examples(self, data_dir):
    """Gets a collection of `InputExample`s for prediction."""
    raise NotImplementedError()

  def get_labels(self):
    """Gets the list of labels for this data set."""
    raise NotImplementedError()

  @classmethod
  def _read_tsv(cls, input_file, quotechar=None):
    """Reads a tab separated value file."""
    with tf.gfile.Open(input_file, "r") as f:
      reader = csv.reader(f, delimiter="\t", quotechar=quotechar)
      lines = []
      for line in reader:
        lines.append(line)
      return lines

class WeiboProcessor(DataProcessor):
  """Processor for the Weibo data set (Multilabel)."""

  def get_train_examples(self, data_dir):
    """See base class."""
    return self._create_examples(
        self._read_tsv(os.path.join(data_dir, "train.tsv")), "train")

  def get_dev_examples(self, data_dir):
    """See base class."""
    return self._create_examples(
        self._read_tsv(os.path.join(data_dir, "dev.tsv")), "dev")

  def get_test_examples(self, data_dir):
    """See base class."""
    return self._create_examples(
      self._read_tsv(os.path.join(data_dir, "test.tsv")), "test")

  def get_labels(self):
    """See base class."""
    labels=[]
    for line in open('/data6/maohui/workspace/data/secondtag_ml/tag_list'):
        tagid = line.strip().split()[2]
        labels.append(tagid)
    return labels

  def _create_examples(self, lines, set_type):
    """Creates examples for the training and dev sets."""
    examples = []
    for (i, line) in enumerate(lines):
      guid = "%s-%s" % (set_type, i)
      text_a = tokenization.convert_to_unicode(line[0])
      label = tokenization.convert_to_unicode(line[1])
      examples.append(
          InputExample(guid=guid, text_a=text_a, text_b=None, label=label))
    return examples

class SentencePairClassificationProcessor(DataProcessor):
  """Processor for the internal data set. sentence pair classification"""
  def __init__(self):
    self.language = "zh"

  def get_train_examples(self, data_dir):
    """See base class."""
    return self._create_examples(
        self._read_tsv(os.path.join(data_dir, "train.tsv")), "train")

  def get_dev_examples(self, data_dir):
    """See base class."""
    return self._create_examples(
        self._read_tsv(os.path.join(data_dir, "dev.tsv")), "dev")

  def get_test_examples(self, data_dir):
    """See base class."""
    return self._create_examples(
        self._read_tsv(os.path.join(data_dir, "test.tsv")), "test")

  def get_labels(self):
    """See base class."""
    return ["0", "1"]

  def _create_examples(self, lines, set_type):
    """Creates examples for the training and dev sets."""
    examples = []
    for (i, line) in enumerate(lines):
      if i == 0:
        continue
      guid = "%s-%s" % (set_type, i)
      label = tokenization.convert_to_unicode(line[0])
      text_a = tokenization.convert_to_unicode(line[1])
      text_b = tokenization.convert_to_unicode(line[2])
      examples.append(
          InputExample(guid=guid, text_a=text_a, text_b=text_b, label=label))
    return examples

def convert_single_example(ex_index, example, label_list, max_seq_length,tokenizer):
  """Converts a single `InputExample` into a single `InputFeatures`."""
  label_map = {}
  for (i, label) in enumerate(label_list):
    label_map[label] = i

  tokens_a = tokenizer.tokenize(example.text_a)
  tokens_b = None
  if example.text_b:
    tokens_b = tokenizer.tokenize(example.text_b)

  if tokens_b:
    # Modifies `tokens_a` and `tokens_b` in place so that the total
    # length is less than the specified length.
    # Account for [CLS], [SEP], [SEP] with "- 3"
    _truncate_seq_pair(tokens_a, tokens_b, max_seq_length - 3)
  else:
    # Account for [CLS] and [SEP] with "- 2"
    if len(tokens_a) > max_seq_length - 2:
      tokens_a = tokens_a[0:(max_seq_length - 2)]

  # The convention in BERT is:
  # (a) For sequence pairs:
  #  tokens:   [CLS] is this jack ##son ##ville ? [SEP] no it is not . [SEP]
  #  type_ids: 0     0  0    0    0     0       0 0     1  1  1  1   1 1
  # (b) For single sequences:
  #  tokens:   [CLS] the dog is hairy . [SEP]
  #  type_ids: 0     0   0   0  0     0 0
  #
  # Where "type_ids" are used to indicate whether this is the first
  # sequence or the second sequence. The embedding vectors for `type=0` and
  # `type=1` were learned during pre-training and are added to the wordpiece
  # embedding vector (and position vector). This is not *strictly* necessary
  # since the [SEP] token unambiguously separates the sequences, but it makes
  # it easier for the model to learn the concept of sequences.
  #
  # For classification tasks, the first vector (corresponding to [CLS]) is
  # used as as the "sentence vector". Note that this only makes sense because
  # the entire model is fine-tuned.
  tokens = []
  segment_ids = []
  tokens.append("[CLS]")
  segment_ids.append(0)
  for token in tokens_a:
    tokens.append(token)
    segment_ids.append(0)
  tokens.append("[SEP]")
  segment_ids.append(0)

  if tokens_b:
    for token in tokens_b:
      tokens.append(token)
      segment_ids.append(1)
    tokens.append("[SEP]")
    segment_ids.append(1)

  input_ids = tokenizer.convert_tokens_to_ids(tokens)

  # The mask has 1 for real tokens and 0 for padding tokens. Only real
  # tokens are attended to.
  input_mask = [1] * len(input_ids)

  # Zero-pad up to the sequence length.
  while len(input_ids) < max_seq_length:
    input_ids.append(0)
    input_mask.append(0)
    segment_ids.append(0)

  assert len(input_ids) == max_seq_length
  assert len(input_mask) == max_seq_length
  assert len(segment_ids) == max_seq_length
  #label_id = label_map[example.label]
  label_id = -1
  if ex_index < 5:
    '''
    tf.logging.info("*** Example ***")
    tf.logging.info("guid: %s" % (example.guid))
    tf.logging.info("tokens: %s" % " ".join(
        [tokenization.printable_text(x) for x in tokens]))
    tf.logging.info("input_ids: %s" % " ".join([str(x) for x in input_ids]))
    tf.logging.info("input_mask: %s" % " ".join([str(x) for x in input_mask]))
    tf.logging.info("segment_ids: %s" % " ".join([str(x) for x in segment_ids]))
    tf.logging.info("label: %s (id = %d)" % (example.label, label_id))
    '''
  feature = InputFeatures(
      input_ids=input_ids,
      input_mask=input_mask,
      segment_ids=segment_ids,
      label_id=label_id)
  return feature

def _truncate_seq_pair(tokens_a, tokens_b, max_length):
  """Truncates a sequence pair in place to the maximum length."""

  # This is a simple heuristic which will always truncate the longer sequence
  # one token at a time. This makes more sense than truncating an equal percent
  # of tokens from each, since if one sequence is very short then each token
  # that's truncated likely contains more information than a longer sequence.
  while True:
    total_length = len(tokens_a) + len(tokens_b)
    if total_length <= max_length:
      break
    if len(tokens_a) > len(tokens_b):
      tokens_a.pop()
    else:
      tokens_b.pop()

def create_int_feature(values):
  f = tf.train.Feature(int64_list=tf.train.Int64List(value=list(values)))
  return f

def create_model(bert_config, is_training, input_ids, input_mask, segment_ids,
                 labels, num_labels, use_one_hot_embeddings):
  """Creates a classification model."""
  model = modeling.BertModel(
      config=bert_config,
      is_training=is_training,
      input_ids=input_ids,
      input_mask=input_mask,
      token_type_ids=segment_ids,
      use_one_hot_embeddings=use_one_hot_embeddings)

  # In the demo, we are doing a simple classification task on the entire
  # segment.
  #
  # If you want to use the token-level output, use model.get_sequence_output()
  # instead.
  output_layer = model.get_pooled_output()

  hidden_size = output_layer.shape[-1].value

  output_weights = tf.get_variable(
      "output_weights", [num_labels, hidden_size],
      initializer=tf.truncated_normal_initializer(stddev=0.02))

  output_bias = tf.get_variable(
      "output_bias", [num_labels], initializer=tf.zeros_initializer())

  with tf.variable_scope("loss"):
    if is_training:
      # I.e., 0.1 dropout
      output_layer = tf.nn.dropout(output_layer, keep_prob=0.9)

    logits = tf.matmul(output_layer, output_weights, transpose_b=True)
    logits = tf.nn.bias_add(logits, output_bias)
    probabilities = tf.nn.sigmoid(logits) # add lmh
    return probabilities


tf.logging.set_verbosity(tf.logging.INFO)
processors = {
  "sentence_pair":SentencePairClassificationProcessor,
  "weibo" :WeiboProcessor,
}
bert_config = modeling.BertConfig.from_json_file(FLAGS.bert_config_file)
task_name = FLAGS.task_name.lower()
print("task_name:",task_name)
processor = processors[task_name]()
label_list = processor.get_labels()
#lines_dev=processor.get_dev_examples("./TEXT_DIR")
index2label={i:label_list[i] for i in range(len(label_list))}
tokenizer = tokenization.FullTokenizer(vocab_file=FLAGS.vocab_file, do_lower_case=FLAGS.do_lower_case)


def main(_):
    pass

# init mode and session
# move something codes outside of function, so that this code will run only once during online prediction when predict_online is invoked.
is_training=False
use_one_hot_embeddings=False
batch_size=1
num_labels=len(label_list)
gpu_config = tf.ConfigProto()
#gpu_config.gpu_options.per_process_gpu_memory_fraction = 0.4
gpu_config.gpu_options.allow_growth = True
sess=tf.Session(config=gpu_config)
model=None
global graph
input_ids_p,input_mask_p,label_ids_p,segment_ids_p=None,None,None,None
#if not os.path.exists(FLAGS.init_checkpoint + "checkpoint"):
if not os.path.exists(FLAGS.init_checkpoint):
    print (FLAGS.init_checkpoint)
    raise Exception("failed to get checkpoint. going to return ")

graph = tf.get_default_graph()
with graph.as_default():
    print("going to restore checkpoint")
    #sess.run(tf.global_variables_initializer())
    input_ids_p = tf.placeholder(tf.int32, [batch_size, FLAGS.max_seq_length], name="input_ids")
    input_mask_p = tf.placeholder(tf.int32, [batch_size, FLAGS.max_seq_length], name="input_mask")
    label_ids_p = tf.placeholder(tf.int32, [batch_size], name="label_ids")
    segment_ids_p = tf.placeholder(tf.int32, [FLAGS.max_seq_length], name="segment_ids")
    probabilities = create_model(
        bert_config, is_training, input_ids_p, input_mask_p, segment_ids_p,
        label_ids_p, num_labels, use_one_hot_embeddings)
    saver = tf.train.Saver()
    saver.restore(sess, tf.train.latest_checkpoint(FLAGS.init_checkpoint))

def getmap():
    id2name = dict()
    for line in open('/data6/maohui/workspace/data/secondtag_ml/tag_list'):
        num, tagname, tagid = line.strip().split('\t')
        id2name[tagid] = tagname
    return id2name

id2name = getmap()

def predict_online(line, fd):
    mid, manual, text = line.strip('\n').split("\t")
    text_a = text
    example= InputExample(guid=0, text_a=text_a)
    feature = convert_single_example(0, example, label_list,FLAGS.max_seq_length, tokenizer)
    input_ids = np.reshape([feature.input_ids],(1,FLAGS.max_seq_length))
    input_mask = np.reshape([feature.input_mask],(1,FLAGS.max_seq_length))
    segment_ids =  np.reshape([feature.segment_ids],(FLAGS.max_seq_length))
    label_ids =[feature.label_id]
    global graph
    with graph.as_default():
        feed_dict = {input_ids_p: input_ids, input_mask_p: input_mask,segment_ids_p:segment_ids,label_ids_p:label_ids}
        possibility = sess.run([probabilities], feed_dict)
        possibility=possibility[0][0] # get first label
        result = np.argwhere(possibility > 0.65)
        pred_list = []
        num = result.shape[0]
        for i in range(num):
            idx = result[i][0]
            tagid = index2label[idx]
            prob = possibility[idx]
#            pred_list.append(tagid + '@' + '%.3f' % prob)
            pred_list.append(tagid)
        pred_tagids = '|'.join(pred_list)
#        for i, prob in enumerate(possibility):
#            if prob > 0.65:
#                pred_list.append(index2label[i] + '@' + '%.3f' % prob)
#                pred_list.append(index2label[i])
#        pred_tagids = '|'.join(pred_list)
        fd.write(pred_tagids + '\t' + mid + '\t' + manual + '\t' + text + '\n')
    return pred_tagids

if __name__ == "__main__":
  filename="data/second_1w_20210911"
  fd = open('%s_result_4layer'% filename, 'w') 
#  fd = open('%s_result'% filename, 'w') 
  for _cnt, line in enumerate(open(filename, 'r')): 
     begin = datetime.datetime.now() 
     label_predict = predict_online(line, fd)
     end = datetime.datetime.now()
     k = end - begin
#     print (str(_cnt) + "\t"+ label_predict + "\t"+ str(possibility) + '\t'+str(k.total_seconds()))


