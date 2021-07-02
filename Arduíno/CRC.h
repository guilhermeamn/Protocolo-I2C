#ifndef CRC_H
#define CRC_H

#include <Arduino.h>

class CRC
{
private:
    String _codeword; // saída
    String _g; // gerador g(x)
    int _n; // n = k + r 
    int _k; // bits de entrada
    int _r;
public:
    CRC() : _codeword(""), _g(""), _n(0), _k(0), _r(0) {}
    ~CRC() {}
    void decoder(String codeword, String g_x)
    {
      Serial.println("----------------Decoder---------------");
      Serial.println("Codeword recebida: " + codeword);
      Serial.println("Gerador: " + g_x);

      _codeword = codeword;
      _g = g_x;
      _r = _g.length() - 1;
      _n = _codeword.length();
      _k = _n - _r;
      
      String resto = divisao(_codeword, _g);
      bool error = false;
      
      for(int i = 0; i < (_k - 1); i++)
      {
          if(resto[i] == '1'){ error = true; }
      }
  
      if(error) Serial.println("d(x) descartada");
      else Serial.println("d(x) aceita");
    }
    String divisao(String a, String b)
    {
      String dividendo = "";
      String divisor = "";
      String quociente = "";
      String resto = "";
      String next = "";
      int i = 0;

      int b_length = b.length();
      for(int k = 0; k < b_length; k++) dividendo += a[k];

      while(i < _n)
      {
          if(dividendo[0] == '1') divisor = _g;
          else if(dividendo[0] == '0')
          {
              divisor = "";
              for(int l = 0; l < b_length; l++) divisor += '0';
          }
  
          for(int j = 1; j < b_length; j++) next += XOR(dividendo[j],divisor[j]);
  
          if(i == 0) i += b_length;
          else i++;
  
          if(i < _n) next += a[i];
  
          dividendo = next;
          next = "";
      }
  
      resto = dividendo;
  
      return resto;  
    }
    char XOR(char a, char b)
    {
      if(a == b) return '0';
      else return '1';  
    }
    /*
     * Limpa todos os atributos
     */
    void clean()
    {
      _codeword = "";
      _g = "";
      _n = 0;
      _k = 0;
      _r = 0;
    }
};

#endif