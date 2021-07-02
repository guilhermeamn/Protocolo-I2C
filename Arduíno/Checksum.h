#ifndef CHECKSUM_H
#define CHECKSUM_H

#include <Arduino.h>

class Checksum
{
public:
    Checksum(int s) : _sum(0), _size(s), _checksum(0) {}
    ~Checksum() {}
    void receptor(int package[])
    {
        Serial.println("------------Receptor--------------");
        Serial.print("Pacote recebido: "); for(int i = 0; i < 6; i++) Serial.print(String(package[i]) + "\t"); Serial.println();
        calculate_sum(package);
        String word = toBinary(_sum);
        //Serial.print("WORD = "); Serial.println(word);
        String s = checksum_sum(word);
        while(s.length() > _size) s = checksum_sum(s);
        //Serial.print("Soma = "); Serial.println(s);
        if(s.length() < 4) s = adjust(s);
        //Serial.print("NOVA SOMA = "); Serial.println(s);
        _checksum = binaryStringToint(complemento(s));
        Serial.print("Checksum = "); Serial.println(_checksum);
        if(_checksum != 0) Serial.println("ERRO: Dados corrompidos");
    }
    /*
     * Faz o cálculo da soma no checksum
     *  Ex.: 11011 -> 1011
     *                +  1
     */
    String checksum_sum(String word)
    {
      int word_length = word.length();
      int n = word_length - _size; // numeros da frente que tem que retirar
      String sup = "";
      String inf = "";
      for(int i = n; i < word_length; i++) sup += word[i]; // numeros que vao somar com os retirados
      if(n > 0) for(int i = 0; i < n; i++) inf += word[i]; // retirados
      else inf = "0"; // se palavra for menor ou igual ao tamanho da palavra inf é 0
      //Serial.print("sup = "); Serial.println(sup);
      //Serial.print("inf = "); Serial.println(inf);
      String s = soma(binaryStringToint(sup),binaryStringToint(inf));
      return s;
    }
    /*
     * Palavras de 4 bits, completa o binário até 4 bits
     */
    String adjust(String s)
    {
      int i = s.length();
      String new_s = "";
      while(i != 4)
      {
        new_s += '0';
        i++;        
      }
      return new_s + s;
    }
    /*
     * Inverte uma string de trás pra frente
     */
    String reverse(String s)
    {
      String r = s;
      for(int i = 0; i < s.length(); i++) r[i] = s[s.length() - 1 - i];
      return r;
    }
    /*
     * Converte string de binário pra int
     * (https://stackoverflow.com/questions/2343099/convert-binary-format-string-to-int-in-c)
     */
    int binaryStringToint(String s)
    {
      char* start = &s[0];
      int total = 0;
      while (*start)
      {
       total *= 2;
       if (*start++ == '1') total += 1;
      }
      return total;
    }
    String soma(int a, int b) { return toBinary(a + b); }
    String complemento(String s)
    {
        String ret = "";
        int t = s.length();
        for(int i = 0; i < t; i++)
        {
            if(s[i] == '0') ret += '1';
            else if(s[i] == '1') ret += '0';
        }
        return ret;
    }
    String toBinary(int n)
    {
        String r;
        while(n != 0) { r = (n % 2 == 0 ? "0" : "1") + r; n /= 2; }
        return r;
    }
    int toDecimal(int n)
    {
        int decimalNumber = 0, i = 0, remainder;
        while (n!=0)
        {
            remainder = n%10;
            n /= 10;
            decimalNumber += remainder*pow(2,i);
            ++i;
        }
        return decimalNumber;
    }
    void calculate_sum(int g[]) { for(int i = 0; i < 6; i++) _sum += g[i]; }
    /*
     * Limpa todos os atributos
     */
    void clean()
    {
      _sum = 0;
      _checksum = 0;
    }
    
private:
    int _sum;
    int _size; // tamanho da palavra
    int _checksum;
};

#endif