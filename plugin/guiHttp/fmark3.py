from markup import *

_original__call__ = element.__call__
def __call__(self, *args, **kwargs):
    _original__call__(self, *args, **kwargs)
    return self
def __exit__(self, *args):
    element.close(self)
def __enter__(self):
    pass
element.__call__ = __call__
element.__exit__ = __exit__
element.__enter__ = __enter__


if __name__ == "__main__":
    ht = page( )

    images = ( 'egg.jpg', 'spam.jpg', 'eggspam.jpg' )

    with ht.div( class_='thumbs' ):
        ht.img( width=60, height=80, src=images, class_='thumb' )

    print ht
