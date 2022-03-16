## About

Create, customize and manage annotations. You have access to your notes on any server the bot is also a part of.

Use your creativity with notes, create game cards, your diary or simply to save some important information.

**UNLIMITED!** Currently you can create **UNLIMITED** annotations with an **UNLIMITED** number of categories/fields in each of them.

### Format of a note

A note has its **name** and **categories** , of which it must have some **text** .

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

### Commands

The bot's **default prefix** is the: **$**

To check **all current commands**, **type $help** in any channel which the bot has permissions.

**Main commands:**
- **Create a new note ( to create a new note it is also necessary to create a field )** 
```
$add <nome_da_nota> <"nome_da_categoria"> <"texto">
```
```
Ex: $add joselito-profile "nick" "Batman"
```
- **List all your notes**
```
$notes
```
- **Show a note**
```
$show <nome_da_nota_existente>
```
```
Ex: $show joselito-profile
```
- **Edit a note category**
```
$edit <nome_da_nota_existente> <"nome_da_categoria_existente"> <"novo_texto">
```
```
Ex: $edit joselito-profile "nick" "Robin"
```
- **Remove a category/field from a note**
```
$rm <nome_da_nota_existente> <"nome_da_categoria_existente">
```
```
Ex: $rm joselito-profile "nick"
```
- **Remove a note**
```
$rm <nome_da_nota_existente>
```
```
Ex: $rm joselito-profile
```

### Contact

Are you having problems? Open an **issue** in the [repositório](https://github.com/davidrezende/haru-bot/) or check the available contact channels on my [github profile](https://github.com/davidrezende)
