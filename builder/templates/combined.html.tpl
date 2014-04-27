<!DOCTYPE html>
<html>
    <head>
        <title>Ответы по госам</title>
        {{ assets }}
    </head>
    <body>
        <h1>{{ discipline }}</h1>
        <section class="questions">
            <h2>Список вопросов</h2>
            {{ questions }}
        </section>
        <section class="answers">
            <h2>Ответы</h2>
            {{ answers }}
        </section> 
        <section class="definitions">
            <h2>Определения</h2>
            {{ definitions }}
        </section>
    </body>
</html>