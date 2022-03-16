## Bem vindo ao HaruBot

Crie, personalize e gerencie anotações. Você tem acesso a suas notas em qualquer servidor em que o bot também faça parte.

Utilize sua criatividade com as notas, crie notas para fichas de jogos, seu diário ou simplesmente para salvar alguma informação importante.

**É ILIMITADO!** Atualmente você pode criar anotações **ILIMITADAS** com um número de categorias/campos **ILIMITADAS** em cada uma delas.

### Formato de uma nota

Uma nota tem seu **nome** e suas **cateogorias**, dais quais devem possuir algum **texto**.

Exemplo:
```
--->note
    --->category1
        --->text
        
    --->(...)    
        
    --->category999
        --->text
        
--->(...)     

--->note999
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
- Criar uma nova nota ( para criar uma nova nota é necessário criar um campo obrigatoriamente )
```
$add <nome_da_nota> <"nome_da_categoria"> <"texto">
```
```
Ex: $add joselito-profile "nick" "Batman"
```
- Listar todas as suas notas
```
$notes
```
- Mostrar uma nota
```
$show <nome_da_nota_existente>
```
```
Ex: $show joselito-profile
```
- Editar uma categoria de uma nota
```
$edit <nome_da_nota_existente> <"nome_da_categoria_existente"> <"novo_texto">
```
```
Ex: $edit joselito-profile "nick" "Robin"
```
- Deletar uma categoria/campo de uma nota
```
$rm <nome_da_nota_existente> <"nome_da_categoria_existente">
```
```
Ex: $rm joselito-profile "nick"
```
- Deletar uma nota
```
$rm <nome_da_nota_existente>
```
```
Ex: $rm joselito-profile
```

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [Basic writing and formatting syntax](https://docs.github.com/en/github/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/davidrezende/haru-bot/settings/pages). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.
