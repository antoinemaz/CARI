# coding: utf8

# page de la liste des budgets
@auth.requires_login()
def gestionBudgets():
    
    # test pour savoir si le user connecté est un president
    isPresident = session.auth.user.group_id == Constantes.PRESIDENT
    
    addBudget = False
    
    # si président : il aura la possibilité d'ajouter un budget
    if(isPresident):
       addBudget = True
    
     # CREATION DU TABLEAU DE TOUS LES BUDGETS
    gridAllBudget = SQLFORM.grid(db.budget, fields=(db.budget.entite_id, db.budget.date_budget,db.budget.Date, db.budget.budget_initial), searchable=False, csv=False, user_signature=False, ui="jquery-ui", links_in_grid=True, create=False, editable=False, deletable=False, details=False, links=[lambda row: A('Detail',_href=URL("budget","detailBudget",vars=dict(idBudget=row.id)))] )
    
    # dictionnaire contenant la liste des derniers budgets en date de chaque entité
    newBudgets = budgetService.getLastBudgets()

    #création d'un formulaire contenant le bouton afin de constituer le fichier csv
    formCsv=FORM(INPUT(_type='submit', _style='margin-top: 8px;', _value='Export CSV'),keepvalues=True)

    # si le bouton du formulaire csv est cliqué
    if formCsv.accepts(request,session):
    
        # constitution du fichier csv a l'aide de l'API XLWT
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
        
        # on parcours tous les budgets (derniers en date de chaque entité) et on va les insérer dans le fichier csv
        for row in newBudgets:
            
            # pour chaque budget, get total de tous les produits du budget
            total = budgetService.getTotalProduitsByBudgetId(row.get('id'))
            
            # pourcentage d'atteinte du budget initial
            pourcentage = budgetService.getPercentValue((total/row.get('budget_initial'))*100,2)
            
            ws.write(i, 0, entiteService.getNameOfEntite(row.get('entite_id')))
            ws.write(i, 1, budgetService.formatDate(row.get('date_budget')))
            ws.write(i, 2, str(row.get('budget_initial'))+' €')
            ws.write(i, 3, (str(row.get('budget_initial') - total)  +' €'))
            ws.write(i, 4, (str(pourcentage) +' %'))
            i += 1
        
        streamIO=cStringIO.StringIO()
        wb.save(streamIO)

        # la response est le fichier test.csv
        response.view='test.csv'
        
        # on construit le nom du fichier (avec le date du jour)
        filename = "export_budget_" + str(datetime.now()).replace(":", "") + '.csv'
        
        # et on retourne le nom du fichier et le flux de type string dans la vue de response.view (test.csv)
        return dict(filename=filename,stream=streamIO)

    # si pas d'export, on retourne la vue de gestion des budgets (par défaut)
    return dict(gridAllBudget=gridAllBudget,newBudgets=newBudgets,addBudget=addBudget,formCsv=formCsv)

# page d'ajout d'un budget
@auth.requires_membership('President')
def addBudget():

    # CREATION DU FORMULAIRE D'AJOUT D'UN BUDGET
    form = SQLFORM(db.budget)

    # SI LE FORMULAIRE EST SOUMISn insertion en base
    if form.process().accepted:
       response.flash = 'form accepted'
        # PUIS ON REDIRIGE VERS LA PAGE DE GESTION DES BUDGETS
       redirect(URL('gestionBudgets'))
    elif form.errors:
       response.flash = 'form has errors'
    else:
       response.flash = 'please fill out the form'
    return locals()

# page de détails d'un budget
@auth.requires_login()
def detailBudget():
    
    # id du budget récuperé en paramètre depuis le requete http
    idBudget = request.vars.idBudget;
    
    if idBudget is not None:
        
            # on va récupérer le budget par son id 
            rowBudget = budgetService.getBudgetById(idBudget)
            
            # et le nom de l'entité par l'id de l'entité récupéré dans le budget
            nameOfEntite = entiteService.getNameOfEntite(rowBudget.entite_id)
    
    # et les produits par le budget_id
    rows = budgetService.getProduitsByBudgetId(idBudget)
    
    # et pour finir, le prix total du budget
    total = budgetService.getTotalProduitsByBudgetId(idBudget)
    
    return locals()
