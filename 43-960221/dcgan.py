import numpy as np
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import os
import matplotlib.pyplot as plt

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def load_data():
    return input_data.read_data_sets('../data/')


def filter(input, digit):
    data = input.train.next_batch(input.train.num_examples)
    labels, images = np.array(data[1], dtype=np.float32), np.array(data[0], dtype=np.float32)
    print(type(images[labels == digit]))
    return images[labels == digit]


def conv2d(input, filter, kernel):
    return tf.nn.conv2d(input, filter, strides=[1, kernel, kernel, 1], padding='SAME')


def pool(input, kernel):
    return tf.nn.max_pool(input, ksize=[1, kernel, kernel, 1], strides=[1, 2, 2, 1],
                          padding='SAME')


def d_out(input, D):
    # 28 28 1
    l1 = conv2d(input, D['CONV_1']['W'], 1)
    l1 = tf.nn.relu(l1 + D['CONV_1']['b'])

    l1 = pool(l1, 2)
    # 14 14 64

    l1 = conv2d(l1, D['CONV_2']['W'], 1)
    l1 = tf.nn.relu(l1 + D['CONV_2']['b'])

    # 14 14 128

    l1 = pool(l1, 2)

    # 7 7 128
    l1 = tf.reshape(l1, [-1, 7 * 7 * 128])
    l1 = tf.nn.relu(tf.add(tf.matmul(l1, D['FC_1']['W']), D['FC_1']['b']))
    l1 = tf.nn.relu(tf.add(tf.matmul(l1, D['FC_2']['W']), D['FC_2']['b']))
    output = tf.nn.sigmoid(tf.add(tf.matmul(l1, D['output']['W']), D['output']['b']))

    return output


def generator_out(G, batch_size, z_dimension):
    z = tf.truncated_normal([batch_size, z_dimension], name='Z')

    ifc1 = tf.nn.relu(tf.add(tf.matmul(z, G['IFC_1']['W']), G['IFC_1']['b']))
    ifc1 = tf.reshape(ifc1, (-1, 56, 56, 1))
    # 56 56 1
    iconv1 = conv2d(ifc1, G['ICONV_1']['W'], 1)
    iconv1 = tf.nn.relu(iconv1 + G['ICONV_1']['b'])
    # 56 56 512
    iconv2 = conv2d(iconv1, G['ICONV_2']['W'], 1)
    iconv2 = tf.nn.relu(iconv2 + G['ICONV_2']['b'])
    # 56 56 256
    iconv2 = pool(iconv2, 2)
    # 28 28 256
    iconv3 = conv2d(iconv2, G['ICONV_3']['W'], 1)
    iconv3 = tf.nn.relu(iconv3 + G['ICONV_3']['b'])
    # 28 28 128
    output = conv2d(iconv3, G['out']['W'], 1)
    output = tf.add(output, G['out']['b'])
    # 28 28 1
    return output


def get_next_batch(data, bz):
    for i in range(int(len(data) / bz)):
        yield data[i * bz: (i + 1) * bz]


def sample_generated_image(gen, save_path):
    with tf.Session() as sess:
        saver = tf.train.Saver()
        saver.restore(sess, save_path)
        return sess.run(generator_out(gen, 3, 100))


def train(data, generator, discriminator, batch_size, z_dim, save_path, initial_step=False):
    images = tf.placeholder('float', shape=[None, 28, 28, 1], name='images')
    gz = generator_out(generator, batch_size, z_dim)
    dx = d_out(images, discriminator)
    dg = d_out(gz, discriminator)
    generator_loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=tf.ones_like(dg), logits=dg))

    d_loss_real = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=tf.ones_like(dx), logits=dx))
    d_loss_fake = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=tf.zeros_like(dg), logits=dg))

    discriminator_loss = d_loss_real + d_loss_fake
    trainable_variables = tf.trainable_variables()

    discriminator_trainable_variables = [var for var in trainable_variables if 'D' in var.name]
    generator_trainable_variables = [var for var in trainable_variables if 'G' in var.name]
    d_fake_opt = tf.train.AdamOptimizer(0.0005).minimize(d_loss_fake, var_list=discriminator_trainable_variables)
    d_real_opt = tf.train.AdamOptimizer(0.0005).minimize(d_loss_real, var_list=discriminator_trainable_variables)
    generator_opt = tf.train.AdamOptimizer(0.0005).minimize(generator_loss, var_list=generator_trainable_variables)
    discriminator_opt = tf.train.AdamOptimizer(learning_rate=0.0005).minimize(discriminator_loss,
                                                                              var_list=discriminator_trainable_variables)
    n_epoch = 1
    with tf.Session() as sess:
        saver = tf.train.Saver()
        if initial_step:
            sess.run(tf.global_variables_initializer())
        else:
            saver.restore(sess, save_path)

        with tf.name_scope('optimization'):
            image_ = filter(data, 8)
            for epoch in range(n_epoch):
                print(epoch, 'th training step...')
                count = 0
                for image in get_next_batch(image_, batch_size):
                    if count % 1 == 0:
                        print(count, 'batch')
                        image = np.reshape(image, [batch_size, 28, 28, 1])
                        sess.run([generator_opt, discriminator_opt], feed_dict={
                            images: image
                        })
                    count += 1

        saver.save(sess, save_path)


discriminator = {
    'CONV_1': {
        'W': tf.Variable(tf.truncated_normal([3, 3, 1, 64], stddev=0.02), name='DC_1_W'),
        'b': tf.Variable(tf.truncated_normal([64]), name='DC_1_b')
    },
    'CONV_2': {
        'W': tf.Variable(tf.truncated_normal([5, 5, 64, 128], stddev=0.02), name='DC_2_W'),
        'b': tf.Variable(tf.truncated_normal([128]), name='DC_2_b')
    },
    'FC_1': {
        'W': tf.Variable(tf.truncated_normal([7 * 7 * 128, 512]), name='DFC_1_W'),
        'b': tf.Variable(tf.truncated_normal([1]), name='DFC_1_b')
    },
    'FC_2': {
        'W': tf.Variable(tf.truncated_normal([512, 1024]), name='DFC_2_W'),
        'b': tf.Variable(tf.truncated_normal([1]), name='DFC_2_b')
    },
    'output': {
        'W': tf.Variable(tf.truncated_normal([1024, 1]), name='DOUT_W'),
        'b': tf.Variable(tf.truncated_normal([1]), name='DOUT_b')
    },
}
generator = {
    'IFC_1': {
        'W': tf.Variable(tf.truncated_normal([100, 7 * 7 * 8 * 8], stddev=0.05), name='GIFC_1_W'),
        'b': tf.Variable(tf.truncated_normal([1]), name='GIFC_1_b')
    },
    'ICONV_1': {
        'W': tf.Variable(tf.truncated_normal([3, 3, 1, 512], stddev=0.05), name='GC_1_W'),
        'b': tf.Variable(tf.truncated_normal([512]), name='GC_1_b')
    },
    'ICONV_2': {
        'W': tf.Variable(tf.truncated_normal([3, 3, 512, 256], stddev=0.05), name='GC_2_W'),
        'b': tf.Variable(tf.truncated_normal([256]), name='GC_2_b')
    },
    'ICONV_3': {
        'W': tf.Variable(tf.truncated_normal([3, 3, 256, 128], stddev=0.05), name='ICONV_3_W'),
        'b': tf.Variable(tf.truncated_normal([128]), name='ICONV_3_b')
    },
    'out': {
        'W': tf.Variable(tf.truncated_normal([3, 3, 128, 1], stddev=0.05), name='out_W'),
        'b': tf.Variable(tf.truncated_normal([1]), name='out_b')
    }
}

data = load_data()
shape = 28
batch_size = 100
z_dim = 100
save_path = '../save/GAN_0/gan_0.ckpt'

train(data, generator, discriminator, batch_size, z_dim, save_path)

images = sample_generated_image(generator, save_path)
for i in range(3):
    plt.imshow(images[i, :, :, 0], cmap='gray')
    plt.show()
