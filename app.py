import os
from flask import Flask, request, render_template, jsonify, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
#
from first import bit_operations as bo
from first import rc4, vernam, des
#
from second import algebra as al
from second import rsa
#
from third import gf_256 as gf
from third import rijndael


UPLOAD_FOLDER = 'files'


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/firstlab')
def first():
    return render_template('first.html')


@app.route('/secondlab')
def second():
    return render_template('second.html')


@app.route('/thirdlab')
def third():
    return render_template('third.html')


@app.route('/getbit', methods=['POST'])
def getbit():
    try:
        if not 0 < len(request.json['a']) <= 32:
            raise ValueError('a length must be in range [1, 32]')

        a = int(request.json['a'], 2)
        k = int(request.json['k'])

        if k < 0 or k > 31:
            raise ValueError('k must be in range [0, 31]')

        res = bo.get_bit(a, k)

        return jsonify({'res': res})
    except Exception as ex:
        return jsonify({'error': str(ex)})


@app.route('/changebit', methods=['POST'])
def changebit():
    try:
        if not 0 < len(request.json['a']) <= 32:
            raise ValueError('a length must be in range [1, 32]')

        a = int(request.json['a'], 2)
        k = int(request.json['k'])

        if k < 0 or k > 31:
            raise ValueError('k must be in range [0, 31]')

        res = bin(bo.change_bit(a, k))[2:]

        return jsonify({'res': res})
    except Exception as ex:
        return jsonify({'error': str(ex)})


@app.route('/swapbits', methods=['POST'])
def swapbits():
    try:
        if not 0 < len(request.json['a']) <= 32:
            raise ValueError('a length must be in range [1, 32]')

        a = int(request.json['a'], 2)
        i = int(request.json['i'])
        j = int(request.json['j'])

        if i < 0 or i > 31:
            raise ValueError('i must be in range [0, 31]')
        if j < 0 or j > 31:
            raise ValueError('j must be in range [0, 31]')

        res = bin(bo.swap_bits(a, i, j))[2:]

        return jsonify({'res': res})
    except Exception as ex:
        return jsonify({'error': str(ex)})


@app.route('/zerobits', methods=['POST'])
def zerobits():
    try:
        if not 0 < len(request.json['a']) <= 32:
            raise ValueError('a length must be in range [1, 32]')

        a = int(request.json['a'], 2)
        k = int(request.json['k'])

        if k < 0 or k > 32:
            raise ValueError('k must be in range [0, 31]')

        res = bin(bo.zero_bits(a, k))[2:]

        return jsonify({'res': res})
    except Exception as ex:
        return jsonify({'error': str(ex)})


@app.route('/gluebits', methods=['POST'])
def gluebits():
    try:
        length = len(request.json['a'])

        if not 0 < length <= 32:
            raise ValueError('a length must be in range [1, 32]')

        a = int(request.json['a'], 2)
        k = int(request.json['k'])

        if k < 0 or k >= length:
            raise ValueError('k must be in range [0, len(a) - 1]')

        res = bin(bo.glue_bits(a, k, length))[2:]

        return jsonify({'res': res})
    except Exception as ex:
        return jsonify({'error': str(ex)})


@app.route('/midbits', methods=['POST'])
def midbits():
    try:
        length = len(request.json['a'])

        if not 0 < length <= 32:
            raise ValueError('a length must be in range [1, 32]')

        a = int(request.json['a'], 2)
        k = int(request.json['k'])

        if k < 0 or 2 * k >= length:
            raise ValueError('k must be in range [0, len(a) / 2]')

        res = bin(bo.get_middle_bits(a, k, length))[2:]

        return jsonify({'res': res})
    except Exception as ex:
        return jsonify({'error': str(ex)})


@app.route('/swapbytes', methods=['POST'])
def swapbytes():
    try:
        if not 0 < len(request.json['a']) <= 64:
            raise ValueError('a length must be in range [1, 64]')

        a = int(request.json['a'], 2)
        i = int(request.json['i'])
        j = int(request.json['j'])

        if i < 0 or i > 7:
            raise ValueError('i must be in range [0, 7]')
        if j < 0 or j > 7:
            raise ValueError('j must be in range [0, 7]')

        res = bin(bo.swap_bytes(a, i, j))[2:]

        return jsonify({'res': res})
    except Exception as ex:
        return jsonify({'error': str(ex)})


@app.route('/maxpow2', methods=['POST'])
def maxpow2():
    try:
        x = int(request.json['x'])

        res = bo.max_div_pow2(x)

        return jsonify({'res': res})
    except Exception as ex:
        return jsonify({'error': str(ex)})


@app.route('/withinrange', methods=['POST'])
def withinrange():
    try:
        x = int(request.json['x'])

        res = bo.within_range(x)

        return jsonify({'res': res})
    except Exception as ex:
        return jsonify({'error': str(ex)})


@app.route('/xorall', methods=['POST'])
def xorall():
    try:
        if not 0 < len(request.json['x']) <= 32:
            raise ValueError('x length must be in range [1, 32]')

        x = int(request.json['x'], 2)

        res = bin(bo.xor_all_bits(x))[2:]

        return jsonify({'res': res})
    except Exception as ex:
        return jsonify({'error': str(ex)})


@app.route('/leftshift', methods=['POST'])
def leftshift():
    try:
        length = len(request.json['a'])

        if not 0 < length <= 32:
            raise ValueError('a length must be in range [1, 32]')

        a = int(request.json['a'], 2)
        k = int(request.json['k'])

        res = bin(bo.cycle_left(a, k, length))[2:]

        return jsonify({'res': res})
    except Exception as ex:
        return jsonify({'error': str(ex)})


@app.route('/rightshift', methods=['POST'])
def rightshift():
    try:
        length = len(request.json['a'])

        if not 0 < length <= 32:
            raise ValueError('a length must be in range [1, 32]')

        a = int(request.json['a'], 2)
        k = int(request.json['k'])

        res = bin(bo.cycle_right(a, k, length))[2:]

        return jsonify({'res': res})
    except Exception as ex:
        return jsonify({'error': str(ex)})


@app.route('/transposebits', methods=['POST'])
def transposebits():
    try:
        length = len(request.json['a'])

        if not 0 < length <= 32:
            raise ValueError('a length must be in range [1, 32]')

        a = int(request.json['a'], 2)
        k = request.json['k'].split(',')

        arr = [int(x) for x in k]

        for x in arr:
            if not 0 <= x <= 32:
                raise ValueError('x in array must be in range [0, 31]')

        res = bin(bo.transpose_bits(a, arr))[2:]

        return jsonify({'res': res})
    except Exception as ex:
        return jsonify({'error': str(ex)})


@app.route('/vernam', methods=['POST'])
def vernam_cipher():
    try:
        data_value = request.files['file']
        key_value = request.files['key']

        if data_value and key_value:
            filename = secure_filename(data_value.filename)
            data = data_value.read()
            key = key_value.read()

            res = vernam.vernam(data, key)
            path = os.path.join(app.config['UPLOAD_FOLDER'], ('(vernam)' + filename))

            with open(path, 'wb') as f:
                f.write(res)

            return jsonify({'path': r'http://localhost:5000/uploads/' + ('(vernam)' + filename)})
        else:
            return jsonify({'error': 'Choose message and key'})
    except Exception as ex:
        return jsonify({'error': str(ex)})


@app.route('/des', methods=['POST'])
def des_cipher():
    try:
        data_value = request.files['file']
        key = request.form['key']
        c0 = request.form['c0']
        mode = request.form['mode']
        decode = request.form['decode']

        if data_value:
            filename = secure_filename(data_value.filename)

            if len(key) != 8:
                raise ValueError('key must be 8 symbols')
            if mode != 'ecb' and len(c0) != 8:
                raise ValueError('c0 must be 8 symbols')

            data = data_value.read()
            des_ = des.DES(des.Mode._bytes_to_block(key.encode('utf-8')))

            if mode == 'ecb':
                alg = des.ECB(des_)
            elif mode == 'cbc':
                alg = des.CBC(des_, des.Mode._bytes_to_block(c0.encode('utf-8')))
            elif mode == 'ofb':
                alg = des.OFB(des_, des.Mode._bytes_to_block(c0.encode('utf-8')))
            elif mode == 'cfb':
                alg = des.CFB(des_, des.Mode._bytes_to_block(c0.encode('utf-8')))

            if decode == 'true':
                res = alg.decode(data)
                while res[-1] == 0:
                    res.pop()
            else:
                res = alg.encode(data)

            path = os.path.join(app.config['UPLOAD_FOLDER'], ('(des)' + filename))

            with open(path, 'wb') as f:
                f.write(res)

            return jsonify({'path': r'http://localhost:5000/uploads/' + ('(des)' + filename)})
        else:
            return jsonify({'error': 'Choose some file'})
    except Exception as ex:
        return jsonify({'error': str(ex)})


@app.route('/rc4', methods=['POST'])
def rc4_cipher():
    try:
        data_value = request.files['file']
        key = request.form['key']

        if data_value:
            filename = secure_filename(data_value.filename)
            data = data_value.read()

            if len(key) == 0:
                raise ValueError('Key size must be more than 0 symbols')

            rc4_ = rc4.RC4()
            res = rc4_.encode(data, key.encode('utf-8'))
            path = os.path.join(app.config['UPLOAD_FOLDER'], ('(rc4)' + filename))

            with open(path, 'wb') as f:
                f.write(res)

            return jsonify({'path': r'http://localhost:5000/uploads/' + ('(rc4)' + filename)})
        else:
            return jsonify({'error': 'Choose some file'})
    except Exception as ex:
        return jsonify({'error': str(ex)})


@app.route('/simplenums', methods=['POST'])
def simplenums():
    try:
        m = int(request.json['m'])
        res = al.get_prime_numbers(m)

        path = os.path.join(app.config['UPLOAD_FOLDER'], f'{m}_simplenums.txt')

        res = [str(x) for x in res]
        ans = ', '.join(res)

        with open(path, 'w') as f:
            f.write(ans)

        return jsonify({'path': r'http://localhost:5000/uploads/' + f'{m}_simplenums.txt'})
    except Exception as ex:
        return jsonify({'error': str(ex)})


@app.route('/rds', methods=['POST'])
def rds():
    try:
        m = int(request.json['m'])
        res = al.rds(m)

        path = os.path.join(app.config['UPLOAD_FOLDER'], f'{m}_rds.txt')

        res = [str(x) for x in res]
        ans = ', '.join(res)

        with open(path, 'w') as f:
            f.write(ans)

        return jsonify({'path': r'http://localhost:5000/uploads/' + f'{m}_rds.txt'})
    except Exception as ex:
        return jsonify({'error': str(ex)})


@app.route('/euler', methods=['POST'])
def euler():
    try:
        x = int(request.json['x'])
        res = al.euler(x)

        return jsonify({'res': res})
    except Exception as ex:
        return jsonify({'error': str(ex)})


@app.route('/factorization', methods=['POST'])
def factorization():
    try:
        m = int(request.json['m'])
        res = al.factorization(m)

        path = os.path.join(app.config['UPLOAD_FOLDER'], f'{m}_factorization.txt')

        res = [str(x) for x in res]
        ans = ' * '.join(res)

        with open(path, 'w') as f:
            f.write(ans)

        return jsonify({'path': r'http://localhost:5000/uploads/' + f'{m}_factorization.txt'})
    except Exception as ex:
        return jsonify({'error': str(ex)})


@app.route('/fastpow', methods=['POST'])
def fastpow():
    try:
        a = int(request.json['a'])
        i = int(request.json['i'])
        j = int(request.json['j'])

        if a < 1:
            raise ValueError('a < 1')
        if i < 1:
            raise ValueError('i < 1')
        if j < 1:
            raise ValueError('j < 1')

        res = al.pow_mod(a, i, j)

        return jsonify({'res': res})
    except Exception as ex:
        return jsonify({'error': str(ex)})


@app.route('/euclid', methods=['POST'])
def euclid():
    try:
        a = int(request.json['a'])
        k = int(request.json['k'])

        if a < 1:
            raise ValueError('a < 0')
        if k < 1:
            raise ValueError('k < 0')

        res = al.euclid(a, k)

        return jsonify({'res': res})
    except Exception as ex:
        return jsonify({'error': str(ex)})


@app.route('/exeuclid', methods=['POST'])
def exeuclid():
    try:
        a = int(request.json['a'])
        k = int(request.json['k'])

        if a < 1:
            raise ValueError('a < 0')
        if k < 1:
            raise ValueError('k < 0')

        res = rsa.euclid_ex_bin(a, k)

        return jsonify({'res': res})
    except Exception as ex:
        return jsonify({'error': str(ex)})


@app.route('/rsa', methods=['POST'])
def rsa_cipher():
    try:
        data_value = request.files['file']
        decode = request.form['decode']

        if data_value:
            filename = secure_filename(data_value.filename)
            data = data_value.read()

            if decode == 'false':
                rsa_ = rsa.RSA()

                enc = bytearray()
                for i in range(0, len(data), 255):
                    enc.extend(rsa_.encode(data[i:i + 255]))

                d, n = rsa_.get_key()

                path = os.path.join(app.config['UPLOAD_FOLDER'], ('(key)' + filename))
                with open(path, 'wb') as f:
                    f.write(d.to_bytes(256, byteorder='little'))
                    f.write(n.to_bytes(256, byteorder='little'))

                path = os.path.join(app.config['UPLOAD_FOLDER'], ('(rsa)' + filename))
                with open(path, 'wb') as f:
                    f.write(enc)

                res = {
                    'path': r'http://localhost:5000/uploads/' + ('(rsa)' + filename),
                    'key': r'http://localhost:5000/uploads/' + ('(key)' + filename)
                }

                return jsonify(res)
            else:
                key_value = request.files['key']
                key = key_value.read()

                if len(key) != 512:
                    raise ValueError("Incorrect key")

                d = int.from_bytes(key[:256], byteorder='little')
                n = int.from_bytes(key[256:], byteorder='little')

                dec = bytearray()
                for i in range(0, len(data), 256):
                    dec.extend(rsa.RSA.decode(data[i:i + 256], d, n))

                while dec[-1] == 0:
                    dec.pop()

                path = os.path.join(app.config['UPLOAD_FOLDER'], ('(rsa)' + filename))
                with open(path, 'wb') as f:
                    f.write(dec)
                return jsonify({'path': r'http://localhost:5000/uploads/' + ('(rsa)' + filename)})
        else:
            return jsonify({'error': 'Choose some file'})
    except Exception as ex:
        return jsonify({'error': str(ex)})


@app.route('/gfpolinom', methods=['POST'])
def gfpolinom():
    try:
        x = int(request.json['x'], 2)

        if not 0 <= x <= 255:
            raise ValueError('x must be in range [0, 255]')

        res = gf.to_polynom_form(x)

        return jsonify({'res': res})
    except Exception as ex:
        return jsonify({'error': str(ex)})


@app.route('/gfmul', methods=['POST'])
def gfmul():
    try:
        a = int(request.json['a'], 2)
        k = int(request.json['k'], 2)

        if not 0 <= a <= 255:
            raise ValueError('a must be in range [0, 255]')
        if not 0 <= k <= 255:
            raise ValueError('k must be in range [0, 255]')

        res = bin(gf.mul(a, k))[2:]

        return jsonify({'res': res})
    except Exception as ex:
        return jsonify({'error': str(ex)})


@app.route('/gfinv', methods=['POST'])
def gfinv():
    try:
        x = int(request.json['x'], 2)

        if not 0 <= x <= 255:
            raise ValueError('x must be in range [0, 255]')

        res = bin(gf.inv(x))[2:]

        return jsonify({'res': res})
    except Exception as ex:
        return jsonify({'error': str(ex)})


@app.route('/rijndael', methods=['POST'])
def rijndael_cipher():
    try:
        data_value = request.files['file']
        key = request.form['key']
        c0 = request.form['c0']
        bs = int(request.form['block_size'])
        mode = request.form['mode']
        decode = request.form['decode']

        if data_value:
            filename = secure_filename(data_value.filename)

            if not bs in [16, 24, 32]:
                raise ValueError('block size must be 16/24/32')
            if not len(key) in [16, 24, 32]:
                raise ValueError('key must be 16/24/32 symbols')
            if mode != 'ecb' and len(c0) != bs:
                raise ValueError('c0 must be the same size as block size')

            data = data_value.read()
            rijndael_ = rijndael.Rijndael((key.encode('utf-8')), bs // 4)

            if mode == 'ecb':
                alg = rijndael.ECB(rijndael_)
            elif mode == 'cbc':
                alg = rijndael.CBC(rijndael_, c0.encode('utf-8'))
            elif mode == 'ofb':
                alg = rijndael.OFB(rijndael_, c0.encode('utf-8'))
            elif mode == 'cfb':
                alg = rijndael.CFB(rijndael_, c0.encode('utf-8'))

            if decode == 'true':
                res = alg.decode(data)
                while res[-1][-1] == 0:
                    res[-1] = res[-1][:-1]
            else:
                res = alg.encode(data)

            path = os.path.join(app.config['UPLOAD_FOLDER'], ('(rd)' + filename))

            with open(path, 'wb') as f:
                for x in res:
                    f.write(x)

            return jsonify({'path': r'http://localhost:5000/uploads/' + ('(rd)' + filename)})
        else:
            return jsonify({'error': 'Choose some file'})
    except Exception as ex:
        return jsonify({'error': str(ex)})


if __name__ == '__main__':
    app.run(debug=True)
