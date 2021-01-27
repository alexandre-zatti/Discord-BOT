import db as database

async def join_acc(ctx,arg1,arg2):
    if(database.insert_acc(arg1,arg2)):
        await ctx.reply('Conta adicionada com sucesso!')
    else:
        await ctx.reply('Falha ao adicionar conta!')