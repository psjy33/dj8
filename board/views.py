from django.shortcuts import render, redirect
from .models import Board, Reply
from django.utils import timezone
from django.core.paginator import Paginator
# Create your views here.
def unlikey(request, bpk):
    return redirect("board:detail", bpk)

def likey(request, bpk):
    b = Board.objects.get(id=bpk)
    b.likey.add(request.user)
    return redirect("board:detail", bpk)

def index(request):
    cate = request.GET.get("cate", "")
    kw = request.GET.get("kw", "")
    pg = request.GET.get("page", 1)
    if kw:
        if cate == "sub":
            b = Board.objects.filter(subject__startswith=kw) # subject 가 kw 인 레코드들을 가져옴
        elif cate == "con":
            b = Board.objects.filter(content__contains=kw) 
        elif cate == "wri":
            try: # 레코드에 존재하지 않는 키워드로 검색을 했을 시 오류 페이지가 뜨게 된다. 그 것을 방지하기 위해 try: except:해줘야한다.
                from acc.models import User  # 아까 7일차(CRUD)에선 CharField로 들어가 있었지만 지금은
                u = User.objects.get(username=kw) # ForeignKey로 들어가 있다. ForeignKey를 배우기 전
                b = Board.objects.filter(writer=u)# 이기도 했고 계정이 없는 게시판이었기 때문에 7일차(CRUD)에서는 CharField로 줬지만 지금은 ForeignKey이기 때문에 레코드 자체로 조사를 해야한다 문자열자체와 레코드들을 비교한다? 안된다. 그래서 User탐색을 먼저 진행해야 한다.(from~import~) 레코드 자체를 뽑아와야하니 u = User.objects.get(username=kw)와 b = Board.objects.filter(writer=u)로 검색한 키워드와 Board의 레코드를 연결시켜주어야 한다.
            except:
                b = Board.objects.none() # 아무것도 안들어가 있다를 표시해주는 것이다. 탐색했는데 없을 시 오류가 뜨기 때문에 넣어준 것이다. 이게 없다면 pag = Paginator(b, 3)에서 b에 탐색한게 없을 시 인자가 들어가질 않아 오류가 뜨게 되는 것이다.
    else:
        b = Board.objects.all()
        
    b = b.order_by('-pubdate') # 게시물 생성했을 때 새로 생성한 게시글이 내림차순으로 보이게해주는 것.
    pag = Paginator(b, 3)
    obj = pag.get_page(pg)
    context = {
        "bset" : obj,
        "cate" : cate,
        "kw" : kw
    }
    return render(request, "board/index.html", context)

def detail(request, bpk):
    b = Board.objects.get(id=bpk)
    r = b.reply_set.all()
    context = {
        "b" : b,
        "rset" : r
    }
    return render(request, "board/detail.html", context)

def delete(request, bpk):
    b = Board.objects.get(id=bpk)
    if b.writer == request.user:
        b.delete()
    else:
        pass # 메세지!!
    return redirect("board:index")

def create(request):
    if request.method == "POST":
        s = request.POST.get("sub")
        c = request.POST.get("con")
        Board(subject=s, content=c, writer=request.user, pubdate=timezone.now()).save()
        return redirect("board:index")
    return render(request, "board/create.html")

def update(request, bpk):
    b = Board.objects.get(id=bpk)
    
    if b.writer != request.user:
        # 메세지
        return redirect("board:index")
    
    if request.method == "POST":
        s = request.POST.get("sub")
        c = request.POST.get("con")
        b.subject, b.content = s,c
        b.save()
        return redirect("board:detail", bpk)
    
    context = {
        "b" : b
    }
    return render(request, "board/update.html", context)

def creply(request, bpk):
    b = Board.objects.get(id=bpk)
    c = request.POST.get("com")
    Reply(board=b, comment=c, replyer=request.user).save()
    return redirect("board:detail", bpk)

def dreply(request, bpk, rpk):
    r = Reply.objects.get(id=rpk)
    if r.replyer == request.user:
        r.delete()
    else:
        pass #  마지막날 메세지
    return redirect("board:detail", bpk)