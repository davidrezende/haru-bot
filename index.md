## About
[![GitHub](https://img.shields.io/badge/Invite%20Leaf%20Card%20to%20your%20server-black)](https://discord.com/api/oauth2/authorize?client_id=952058655979749416&permissions=326417770496&scope=bot)

Create, customize and manage annotations. You have access to your notes on any server the bot is also a part of.

Use your creativity with notes, create game cards, your diary or simply to save some important information.

**UNLIMITED!** Currently you can create **UNLIMITED** annotations with an **UNLIMITED** number of categories/fields in each of them.

### Format of notes

A note has its **name** and **categories** , of which it must have some **text** .

```
note
    category1
             text       
    ...         
    category999
             text        
...     
note999
    category1
             text     
    ...         
    category999
             text
```

### Commands

The bot's **default prefix** is the: **$**

To check **all current commands**, **type $help** in any channel which the bot has permissions.

**Main commands:**
- **Create a new note ( to create a new note it is also necessary to create a field )** 
```
$add <name_of_note> <"name_of_category"> <"text">
```
```
Ex: $add bruce-profile "nick" "Batman"
```
- **List all your notes**
```
$notes
```
- **Show a note**
```
$show <name_of_note>
```
```
Ex: $show bruce-profile
```
- **Edit a note category**
```
$edit <name_of_note_exists> <"name_of_category_exists"> <"new_text">
```
```
Ex: $edit bruce-profile "nick" "Robin"
```
- **Remove a category/field from a note**
```
$rm <name_of_note_exists> <"name_of_category_exists">
```
```
Ex: $rm bruce-profile "nick"
```
- **Remove a note**
```
$rm <name_of_note_exists>
```
```
Ex: $rm bruce-profile
```

### Card Customizing

You can customize your annotation with **_thumbnail_** and **_image_**. By default, **all notes have these categories protected**, for customizing the card.

**Adding a _thumbnail_ to the card**
```
$add <name_of_note> thumbnail <"link_of_thumbnail">
```
```
Ex: $add bruce-profile thumbnail "https://i.pinimg.com/736x/a4/10/67/a41067633a6725f2d10edda14764b65f.jpg"
```
**Adding a _image_ to the card**
```
$add <name_of_note> image <"link_of_image">
```
```
Ex: $add bruce-profile image "https://i.pinimg.com/originals/59/e0/58/59e05871554be1987c3974fc98035490.jpg"
```
### Contact

Are you having problems? Open an **issue** in the [repository](https://github.com/davidrezende/haru-bot/) or check the available contact channels on my [github profile](https://github.com/davidrezende)

[![GitHub](https://img.shields.io/github/followers/davidrezende?style=social)](https://github.com/login?return_to=https%3A%2F%2Fgithub.com%2Fdavidrezende)

