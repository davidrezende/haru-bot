## Sobre

Crie, personalize e gerencie anotações. Você tem acesso a suas notas em qualquer servidor em que o bot também faça parte.

Utilize sua criatividade com as notas, crie fichas de jogos, seu diário ou simplesmente para salvar alguma informação importante.

**ILIMITADO!** Atualmente você pode criar anotações **ILIMITADAS** com um número de categorias/campos **ILIMITADAS** em cada uma delas.

### Formato de uma nota

Uma nota tem seu **nome** e suas **categorias**, dais quais devem possuir algum **texto**.

```
note
--->category1
    --->text
        
--->(...)    
        
--->category999
    --->text
        
(...)     

note999
--->category1
    --->text
        
--->(...)    
        
--->category999
    --->text
```

### Comandos

O **prefixo padrão** do bot é o: **$**

Para verificar **todos os comandos** atuais, digite **$help** em algum canal o qual o bot tenha permissões.

**Principais comandos:**
- **Criar uma nova nota** ( **para criar uma nova nota é necessário criar também um campo** )
```
$add <nome_da_nota> <"nome_da_categoria"> <"texto">
```
```
Ex: $add joselito-profile "nick" "Batman"
```
- **Listar todas as suas notas**
```
$notes
```
- **Mostrar uma nota**
```
$show <nome_da_nota_existente>
```
```
Ex: $show joselito-profile
```
- **Editar uma categoria de uma nota**
```
$edit <nome_da_nota_existente> <"nome_da_categoria_existente"> <"novo_texto">
```
```
Ex: $edit joselito-profile "nick" "Robin"
```
- **Deletar uma categoria/campo de uma nota**
```
$rm <nome_da_nota_existente> <"nome_da_categoria_existente">
```
```
Ex: $rm joselito-profile "nick"
```
- **Deletar uma nota**
```
$rm <nome_da_nota_existente>
```
```
Ex: $rm joselito-profile
```

### Contato

Está tendo problemas? Abra uma **issue** no [repositório](https://github.com/davidrezende/haru-bot/) ou verifique os canais de contato disponíveis no meu perfil do [github](https://github.com/davidrezende)
