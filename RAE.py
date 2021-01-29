# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 12:21:04 2021

@author: @BrutalSphere
@contact: e-mail= frantomasgarciaruiz@gmail.com/ftgarrui@inf.upv.es, github = BrutalSphere
"""
class DRAE:
    
    def search(word, disable_errors=False):
        '''
        
        Parameters
        ----------
        word :  string
            As it says It is just a word that you want to find its meaning
            
        disable_errors : boolean, optional
            In case you don't want disturbing messages on your terminal 
            you can disable error messages The default is False.


        Returns
        -------
        Busqueda Object or BusquedaG Object or None (in case of error)
            As the last method returns an object of type Busqueda that allows obtaining definitions 
            and expressions of a word or multiple words using methods

        '''
        from requests import get  as gt #to do web requests
        from bs4 import BeautifulSoup as bs #to do web scraping with html server response
        params = {'m':'form'} 
        '''
        #m indicates the type of search on the RAE website, in this it is a standard search and is used
        as an argument in the web request
        '''
        response = gt("https://dle.rae.es/"+str(word), params=params) #web request and response
        soup=bs(response.content,"lxml") #Declares a soup type object
        if len(soup.find_all('p'))==0 and len(soup.find_all('dic', class_='h1'))==0: #Searches alternatives and definitions
            if disable_errors ==False:
                print(word, ' NO existe en la RAE, y tampoco se ofrecen alternativas') #Error message when there are not alternatives
            return None
        elif len(soup.find_all('n1'))>0: #Searches alternatives
            if disable_errors ==False:
                print(word, ' NO existe en la RAE, pero se ofrecen alternativas') #Error message where there are alternatives
            return BusquedaG(soup)
        return Busqueda(soup)
        
    def exact(word, disable_errors=False):
        '''
        
        Parameters
        ----------
        word : string
            As it says It is just a word that you want to find its meaning
            
            
        disable_errors : boolean, optional
            In case you don't want disturbing messages on your terminal 
            you can disable error messages The default is False.

            
        Returns
        -------
        Busqueda Object or None(in case of error)
            DESCRIPTION.
            As the previous method, Returns a Busqueda type object that allows 
            obtaining definitions and expressions for one exact word

        '''
        from requests import get as gt
        from bs4 import BeautifulSoup as bs
        params = {'m':'30_2'} #m indicates the type of search in RAE web page
        response = gt("https://dle.rae.es/" + word, params=params) #web request and response
        soup=bs(response.content,"lxml") #Declares a soup type object
        if len(soup.find_all('p'))==0: #Searches definitions
            if disable_errors ==False:
                print('El termino ',word, ' NO existe en la RAE') #Error message when the word is not found
            return None
        else:
            return Busqueda(soup)
        
    def starts(word, disable_errors=False):
        '''
        
        Parameters
        ----------
        word : string.
            The prefix of the obtained words
            
        disable_errors : boolean, optional
            In case you don't want disturbing messages on your terminal 
            you can disable error messages. The default is False.

        Returns
        -------
        BusquedaG or None(in case of error)
            Returns a BusquedaG type object that allows 
            obtaining definitions and expressions for multiple words
            
        '''
        from requests import get as gt
        from bs4 import BeautifulSoup as bs
        params = {'m':'31'} #m indicates the type of search in RAE web page
        response = gt("https://dle.rae.es/"+word, params=params) #web request and response
        soup=bs(response.content,"lxml") #Declares a soup type object
        soup = soup.find('div', class_="item-list")  
        if len(soup.find_all('div', class_="n1"))==0: #Search the words that start with the given prefix in the website response
            if disable_errors ==False:
                print('NO existen terminos empezados por ', word) #There are no words that start with the given prefix
            return None
        return BusquedaG(soup)        
        
    def ends(word, disable_errors=False):
        '''

        Parameters
        ----------
        word : string
            The sufix of the obtained words
        disable_errors : TYPE, optional
            In case you don't want disturbing messages on your terminal 
            you can disable error messages. The default is False.

        Returns
        -------
        BusquedaG or None(in case of error)
            Returns a BusquedaG type object that allows 
            obtaining definitions and expressions for multiple words

        '''
        from requests import get as gt
        from bs4 import BeautifulSoup as bs
        params = {'m':'32'} #m indicates the type of search in RAE web page
        response = gt("https://dle.rae.es/"+word, params=params) #web request and response
        soup=bs(response.content,"lxml") #Declares a soup type object
        soup = soup.find('div', class_="item-list")
        if len(soup.find_all('div', class_="n1"))==0: #Search the words that ends with the given sufix in the website response
            if disable_errors ==False:
                print('NO existen terminos terminados en ', word) #There are no words that ends with the given sufix
            return None
        return BusquedaG(soup)        
        
    def contains(word, disable_errors=False):
        '''

        Parameters
        ----------
        word : string
            Characters contained in the words obtained
        disable_errors : boolean, optional
            In case you don't want disturbing messages on your terminal 
            you can disable error messages. The default is False.
            
        Returns
        -------
        BusquedaG or None(in case of error)
            Returns a BusquedaG type object that allows 
            obtaining definitions and expressions for multiple words

        '''
        from requests import get as gt
        from bs4 import BeautifulSoup as bs
        params = {'m':'33'}
        response = gt("https://dle.rae.es/" + word, params=params)
        soup=bs(response.content,"lxml")
        soup = soup.find('div', class_="item-list")
        if len(soup.find_all('div', class_="n1"))==0:
            if disable_errors ==False:
                print('NO existen terminos que contengan ', word)
                print('NO existen terminos que contengan ', word)
            return None
        return BusquedaG(soup)        
        
    def anagram(word, disable_errors=False):
        '''

        Parameters
        ----------
        word : string
            Search word for anagrams
        disable_errors : boolean, optional
            In case you don't want disturbing messages on your terminal 
            you can disable error messages. The default is False.
            
        Returns
        -------
        BusquedaG or None(in case of error)
            Returns a BusquedaG type object that allows 
            obtaining definitions and expressions for multiple words

        '''
        from requests import get as gt
        from bs4 import BeautifulSoup as bs
        params = {'m':'anagram'}
        response = gt("https://dle.rae.es/"+word, params=params)
        soup=bs(response.content,"lxml")
        soup = soup.find('div', class_="item-list")
        if len(soup.find_all('div', class_="n1"))==0:
            if disable_errors ==False:
                print('NO existen terminos que sean anagramas de ', word)
            return None
        return BusquedaG(soup) 
    
class Busqueda:
    from bs4 import BeautifulSoup
    def __init__(self,soup):
        '''

        Parameters
        ----------
        soup : BeautifulSoup object
            Stores the necessary information from the website response

        Returns
        -------
        None.

        '''
        self._word, self._definitions, self._expressions  = self.__buildclass_(soup) #Stores all the information obtained in local parameters
        
    def allIn(self):
        return {'definitions':self._definitions, 'expressions':self._expressions} #Returns all the information stored
        
    def define(self):
        return self._definitions #Returns all the definitions stored
    
    def expression(self):
        return self._expressions #Returns all the expressions stored
    
    def word(self):
        return self._word #Returns the word stored in the objetc
    
    def __buildclass_(self, soup):
        '''
        

        Parameters
        ----------
        soup : BeautifulSoup object
            Stores the necessary information from the website response

        Returns
        -------
        word : String
            The searched word
        definitions : Dict
            All the definitions of the searched word
        dict
            All the expressions of the searched word

        '''
        results = soup.find('div', id= 'resultados')
        definitions = []
        key_exp = [] #Expresions keys
        value_exp = [] #Expresions meanings/values
        word = results.find('header',class_='f').text
        
        for txt in results.find_all('p'):
            '''
            Uses the atributtes to obtain the information
            '''
            if 'class' in txt.attrs:
                if txt['class'][0][0]=='j':
                    definitions.append(txt.text)
                elif txt['class'][0][0]=='k':
                    key_exp.append(txt.text)
                elif txt['class'][0][0]=='m' :
                    value_exp.append(txt.text)
                
        return word, definitions, {i[0]: i[1] for i in zip(key_exp, value_exp)}

class BusquedaG():
    from bs4 import BeautifulSoup
    r = DRAE() #Declares a search dictionary
    def __init__(self,soup):
        self._words = self.__buildclass_(soup) #
        
    def allIns(self):
        return self._words #Returns all the information from all the words stored
        
    def defines(self):
        return {key:value['definitions'] for key, value in self.allIns() } #Returns the definitions from all the words stored
        
    def expressions(self):
        return {key:value['expressions'] for key, value in self.allIns() } #Returns the expressions from all the words stored
        
    def words(self):
        return [key for key in self.allIns()] #Returns all the words stored
        
    def allIn(self, palabra):
        '''

        Parameters
        ----------
        palabra : string
            The searched word

        Raises
        ------
        KeyError
            Raises an error when the searched word is not found in the object

        Returns
        -------
        Dict
            Returns all the information about the searched word

        '''
        try:
            return self._words[palabra]
        except:
            raise KeyError(palabra,'not found')
    
    def define(self, palabra):
        '''

        Parameters
        ----------
        palabra : string
            The searched word

        Raises
        ------
        KeyError
            Raises an error when the searched word is not found in the object

        Returns
        -------
        Dict
            Returns the definitions of the searched word

        '''
        try:
            return self._words[palabra]['definitions']
        except:
            raise KeyError(palabra,'not found')
        
    def expression(self, palabra):
        '''

        Parameters
        ----------
        palabra : string
            The searched word

        Raises
        ------
        KeyError
            Raises an error when the searched word is not found in the object

        Returns
        -------
        Dict
            Returns the expressions about the searched word

        '''
        try:
            return self._words[palabra]['expressions']
        except:
            raise KeyError(palabra,'not found')        
        
    def __buildclass_(self, soup):
        '''
        

        Parameters
        ----------
        soup : BeautifulSoup
            Contains the necessary information from the website response

        Returns
        -------
        res : Dict
            Contains all the information from all the words extracted from
            the soup

        '''
        res = {}
        dicc = DRAE
        
        for txt in soup.find_all('a', href=True):
            word = dicc.exact(txt.get('href')[1:]) #Extracts the word 
            res[word.word()] = word.allIn() 
        return res
