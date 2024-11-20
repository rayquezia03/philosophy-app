from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse


def home(request):
    return render(request, 'index.html')

class Celula():
  item = None
  proximo = None

  def __init__(self,valor):
      self.item = valor

class Fila:
  inicio = None
  fim = None

  def __init__(self):
    self.inicio = None
    self.fim = None

  def EstaVazia(self):
    return self.inicio == None

  def inserir(self,valor):
    c = Celula(valor)
    if self.EstaVazia():
      self.fim = c
      self.inicio = c
    else:
      self.fim.proximo = c
      self.fim = c

  def remover(self):
    if self.EstaVazia():
      return None
    else:
      aux = self.inicio
      valor = self.inicio.item
      self.inicio = self.inicio.proximo
      return valor, aux
  
  def resetar(self):
    self.inicio = None
    self.fim = None

  def imprimir(self):
    aux = self.inicio
    list = []
    while aux != None:
      # print(aux.item)
      list.append(aux.item)
      aux = aux.proximo
      
    return list

def add_client_to_queue(fila,data_client):
    fila.inserir(data_client)
    
def complete_current_customer_service(fila):
    removed_client = fila.remover()
    return removed_client

queue_service = Fila()
all_clients_served = []

#POST do client na fila
def agendar(request):
    print(request.method)
    if request.method == 'POST':
        nome = request.POST['name']
        servico = request.POST.getlist('servico')
        email = request.POST['email']
        celular = request.POST['celular']
        
        data_client = {
            'name': nome,
            'servico': servico,
            'email': email,
            'celular': celular,
            'served': False
        }
        
        add_client_to_queue(queue_service,data_client)
        all_clients_served.append(data_client) 
        
        client_name = data_client['name']
        client_services = data_client['servico']
   
        print('$$$$$$$$$$$$$$$$$$')
        print(queue_service.imprimir())
        
        # return render(request, 'sucess.html', {'client_name': client_name,'client_services':client_services})
        return JsonResponse({'success': True, 'client_name': client_name, 'client_services':client_services})
    else:
        return render(request, 'scheduler.html')

#GET da fila de pessoas que estão em espera
def get_queue(request):
  if queue_service.EstaVazia() != True:
    client_names = []
    
    print('!!!!!!!!!!!!!!!!!')
    print(queue_service.EstaVazia())
    print(queue_service.imprimir())
    
    people_in_stand_by = queue_service.imprimir()
    for i in range(0,len(people_in_stand_by)):
      name = people_in_stand_by[i]['name']
      client_names.append(f'{i+1} - {name}')
    print('#############')
    print(client_names)
    return render(request, "get_queue.html", {'people_in_stand_by': client_names })
  else:
    client_names = None
    return render(request, "get_queue.html", {'people_in_stand_by': client_names })

#DELETE - concluir atendimento/remover cliente da fila
def complete_current_customer_service(request):
    if queue_service.EstaVazia() != True:
      queue = queue_service.imprimir()
      queue[0]['served'] = True
      current_client = queue[0]['name']
      
      queue_service.remover()
      # return JsonResponse({'success': True, 'current_client': current_client})
      return render(request, "complete_current_customer_service.html",{'current_client': current_client})
    else:
      current_client = None
      return render(request, "complete_current_customer_service.html",{'current_client': current_client})
  
#fornecer clientes que ja foram atendidas - "served" == True
def get_queue_completed(request):
  finished_clients = []
  total_workday_clients = 0
  client_names = []
  if all_clients_served != None:
    for client in all_clients_served:
      print('***********')
      print(client)
      if client['served'] == True:
        finished_clients.append(client)
        total_workday_clients = total_workday_clients + 1
      
      for i in range(0,len(finished_clients)):
        client_names.append(finished_clients[i]['name'])
        
      print('------')
      print(finished_clients)
      
    return render(request, "get_queue_completed.html", {'finished_clients': set(client_names) })
  else: 
    client_names = None
    return render(request, "get_queue_completed.html", {'finished_clients': set(client_names) })
    
#reseta a fila de atendimento
def complete_workday(request):
    queue_service.resetar()
    return JsonResponse({'success': True})
  