# coding: utf8
@auth.requires_login()
def gestionBudgets():
    
    isPresident = session.auth.user.group_id == Constantes.PRESIDENT
    
    addBudget = False
    if(isPresident):
       addBudget = True
    
     # CREATION DU TABLEAU DE TOUS LES BUDGETS
    gridAllBudget = SQLFORM.grid(db.budget, fields=(db.budget.entite_id, db.budget.date_budget,db.budget.Date, db.budget.budget_initial), searchable=False, csv=False, user_signature=False, ui="jquery-ui", links_in_grid=True, create=False, editable=False, deletable=False, details=False, links=[lambda row: A('Detail',_href=URL("budget","detailBudget",vars=dict(idBudget=row.id)))] )
    
    newBudgets = db.executesql('SELECT * FROM budget b1 WHERE date_budget = (SELECT max(date_budget) FROM budget b2 WHERE b1.entite_id = b2.entite_id);', as_dict=True)
    
    return dict(gridAllBudget=gridAllBudget,newBudgets=newBudgets,addBudget=addBudget)

@auth.requires_membership('President')
def addBudget():

    # CREATION DU FORMULAIRE D'AJOUT D'UNE COMPOSANTE
    form = SQLFORM(db.budget)

    # SI LE FORMULAIRE EST SOUMIS
    if form.process().accepted:
        # INSERTION EN BASE
       response.flash = 'form accepted'
        # PUIS ON REDIRIGE VERS LA PAGE DE GESTION DES COMPOSANTES
       redirect(URL('gestionBudgets'))
     # SI LE FORMULAIRE CONTIENT DES ERREURS
    elif form.errors:
        # ON VA LES AFFICHER
       response.flash = 'form has errors'
    else:
        # FORMULAIRE VIDE
       response.flash = 'please fill out the form'
    return locals()

@auth.requires_login()
def detailBudget():
    idBudget = request.vars.idBudget;
    
    if idBudget is not None:
            rowBudget = budgetService.getBudgetById(idBudget)
            nameOfEntite = entiteService.getNameOfEntite(rowBudget.entite_id)
    
    rows = budgetService.getProduitsByBudgetId(idBudget)
    
    return locals()

@auth.requires_membership('President')
def export2Budget():
    exportBudget = db().select(db.budget.ALL)
    
    import xlwt
    #from tkFileDialog import asksaveasfilename
    from datetime import datetime
    
    font0 = xlwt.Font()
    font0.name = 'Times New Roman'
    font0.colour_index = 2
    font0.bold = True
    
    style0 = xlwt.XFStyle()
    style0.font = font0
    
    style1 = xlwt.XFStyle()
    style1.num_format_str = 'DD-MM-YY'
    
    wb = xlwt.Workbook()
    ws = wb.add_sheet('ALL_Budgets')
    ws.write(0, 0, 'ID', style0)
    ws.write(0, 1, 'Date', style0)
    ws.write(0, 2, 'Budget initial', style0)
    ws.write(0, 3, 'Entite', style0)
    i = 1
    
    now = datetime.now()
    for row in exportBudget:
        ws.write(i, 0, row.id)
        ws.write(i, 1, now.strftime("%Y-%m-%d %H:%M:%S"))
        ws.write(i, 2, row.budget_initial)
        ws.write(i, 3, entiteService.getNameOfEntite(row.entite_id))
        i += 1
    
    
    
    wb.save('example2.xls')
    
    response.download(request, db.budget)
    
    #response.headers['Content-Type']='application/vnd.ms-excel'
    #response.headers['Content-disposition']='attachment; filename=' +wb
#    response.write(stream.getvalue(), escape=False)
    return locals()
