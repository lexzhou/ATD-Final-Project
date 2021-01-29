# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 12:21:04 2021

@author: @BrutalSphere
@contact: e-mail= frantomasgarciaruiz@gmail.com/ftgarrui@inf.upv.es, github = BrutalSphere
"""
from flask import Flask, jsonify, abort
from RAE import DRAE as dicc
app = Flask(__name__)

json = {}

@app.route("/exacta/<palabra>", methods=['GET'])
def getExactTerm(palabra):
    ### Extract the information about a given word using getExactTerm for dummies
    res = None
    if palabra not in json:
        res = dicc.exact(palabra).allIn()
        if res is None:
            abort(404, 'Word Not Found')
        else:
            json[palabra] = res
    return jsonify({palabra:json[palabra]})

@app.route("/empieza_por/<palabra>", methods=['GET'])
def startsWith(palabra):
    ### Extract the information about a given prefix using startsWith for dummies
    term = dicc.starts(palabra)
    if term is None:
        abort(404, 'No Word Starts With '+ palabra)
    res = term.allIns()
    json.update(res)
    return jsonify(res)

@app.route("/termina_en/<palabra>", methods=['GET'])
def endsWith(palabra):
    ### Extract the information about a given sufix using endsWith for dummies
    term = dicc.ends(palabra)
    if term is None:
        abort(404, 'No Word Ends With '+ palabra)
    res = term.allIns()
    json.update(res)
    return jsonify(res)

@app.route("/contiene/<palabra>", methods=['GET'])
def contains(palabra):
    ### Extract the information about words that contains a given group of characters using contains for dummies
    term = dicc.contains(palabra)
    if term is None:
        abort(404, 'No Word Contains '+ palabra)
    res = term.allIns()
    json.update(res)
    return jsonify(res)

@app.route("/anagrama/<palabra>", methods=['GET'])
def anagram(palabra):
    ### Extract the information about anagrams from a given word using anagram for dummies
    term = dicc.anagram(palabra)
    if term is None:
        abort(404, 'No Word Is An Anagram Of '+ palabra)
    res = term.allIns()
    json.update(res)
    return jsonify(res)
app.run(port =8080)