# coding: utf8
@auth.requires_login()
def gestionBudgets():
    
    isPresident = session.auth.user.group_id == Constantes.PRESIDENT
    
    addBudget = False
    if(isPresident):
       addBudget = True
    
     # CREATION DU TABLEAU DE TOUS LES BUDGETS
    gridAllBudget = SQLFORM.grid(db.budget, fields=(db.budget.entite_id, db.budget.date_budget,db.budget.Date, db.budget.budget_initial), searchable=False, csv=False, user_signature=False, ui="jquery-ui", links_in_grid=True, create=False, editable=False, deletable=False, details=False, links=[lambda row: A('Detail',_href=URL("budget","detailBudget",vars=dict(idBudget=row.id)))] )
    
    newBudgets = budgetService.getLastBudgets()

    formCsv=FORM(INPUT(_type='submit', _style='margin-top: 8px;', _value='Export CSV'),keepvalues=True)

    if formCsv.accepts(request,session):
        exportBudget = db().select(db.budget.ALL)
    
        import cStringIO
        import csv
        import xlwt
        from datetime import datetime
        
        font0 = xlwt.Font()
        font0.name = 'Times New Roman'
        font0.colour_index = 2
        font0.bold = True
        
        style0 = xlwt.XFStyle()
        style0.font = font0
        
        style1 = xlwt.XFStyle()
        style1.num_format_str = 'DD-MM-YY'
        
        wb = xlwt.Workbook(encoding="UTF-8")
        ws = wb.add_sheet('ALL_Budgets')
        ws.write(0, 0, 'Nom de l\'entité', style0)
        ws.write(0, 1, 'Date du budget', style0)
        ws.write(0, 2, 'Budget initial', style0)
        ws.write(0, 3, 'Budget restant', style0)
        ws.write(0, 4, 'Consommation', style0)
        i = 1
        
        now = datetime.now()
        for row in newBudgets:
            
            total = budgetService.getTotalProduitsByBudgetId(row.get('id'))
            pourcentage = budgetService.getPercentValue((total/row.get('budget_initial'))*100,2)
            
            ws.write(i, 0, entiteService.getNameOfEntite(row.get('entite_id')))
            ws.write(i, 1, budgetService.formatDate(row.get('date_budget')))
            ws.write(i, 2, str(row.get('budget_initial'))+' €')
            ws.write(i, 3, (str(row.get('budget_initial') - total)  +' €'))
            ws.write(i, 4, (str(pourcentage) +' %'))
            i += 1
        
        streamIO=cStringIO.StringIO()
        wb.save(streamIO)

        response.view='test.csv'
        
        filename = "export_budget_" + str(datetime.now()).replace(":", "") + '.csv'
        
        return dict(filename=filename,stream=streamIO)

    return dict(gridAllBudget=gridAllBudget,newBudgets=newBudgets,addBudget=addBudget,formCsv=formCsv)

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
    
    total = budgetService.getTotalProduitsByBudgetId(idBudget)
    
    return locals()
