from typing import Optional
from uuid import UUID, uuid4
from base64 import urlsafe_b64encode, urlsafe_b64decode


def wid(*args, keep_order: Optional[bool] = False, **kwargs):
    """
    wee double_u id [WID]
    
    just call wid() to get a WID [wee double_u id]
    
    a wee double_u id [WID] is a lossless short format UUID [universally unique identifier]
    or more precisely a urlsafe 64 bit encoded UUID [version 4]
    with the equal sign padding removed and the final string values reordered
    to ensure the string does not start or end with an underscore '_' or a minus '-'

    optional params: 
     • wid() - no params - defaults to using uuid4()
     • wid(<UUID>) - provide your own UUID instance to convert to WID format
     • wid(<UUID __init__ args & kwargs>) - args & kwargs are passed through to create a UUID
     • wid(keep_order=True) - overrides default behavior of reordering the final WID string
          [keep_order works with all param options]

    if keep_order == False [default: False] we reorder the returned WID string  
    to ensure a WID created with uuid4 does not start or end 
    with an underscore '_' or a minus '-' 
    for each WID keep_order should have the same value 
    when creating a WID and converting a WID back to a UUID 
    it is up to the coder to keep track of WID keep_order usage
    easiest thing to do is just use the default and you should be good
    
    FUN FACTS:
    with a version 4 UUID certain positions have limited values:
    
    example:
    5403468f-8bae-4459-a0e0-89df852b30bc
    XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
                  │    │
    only 4 ───────┘    │
    only 8, 9, a, b ───┘               
    
    [index starts at 0]
    * index 14 is always 4
    * index 19 is limited to 8, 9, a, or b

    when we convert the version 4 UUID as bytes with urlsafe_b64encode we see these limits:
    
    example:
    7dQVF2jKQY-GtcDv-WfSIg==
    XXXXXXXXXXXXXXXXXXXXXX==
            │ │          │
    Q,R,S,T ┘ │          │
              │          │
    A,Q,g,w ──┼──────────┘
              │
    ┌─────────┴───────────────────┐
    -,2,6,C,G,K,O,S,W,a,e,i,m,q,u,y

    [index starts at 0]
    * index 8 is limited to Q, R, S, or T 
    * index 10 is limited to -, 2, 6, C, G, K, O, S, W, a, e, i, m, q, u, or y
    * index 21 is limited to 8, 9, a, b 
      because the 32 hex values do not perfectly match up with 22 base 64 values, 
      this relates to the double equal sign padding

    we can ensure our WID does not start or end with 
    an underscore '_' or a minus '-' by 
    reversing the order of the first 9 values in the string
    considering this desirable we make this the default
    this default is defined by keep_order=False in the signature
    """
    if args and isinstance(args[0], UUID):
        u = args[0]
    elif any(args) or any(kwargs):
        u = UUID(*args, **kwargs)
    else:
        u = uuid4()
    u = urlsafe_b64encode(u.bytes).decode().replace('=', '')
    if keep_order == False:
        return u[:9][::-1] + u[9:22]
    else:
        return u

def wid_to_uuid(w: str, keep_order: Optional[bool] = False) -> UUID:
    """
    just call wid_to_uuid(wid_str) to convert a WID string [wee double_u id] to a UUID instance 

    optional params: 
     • wid(wid_str) - reorders WID string back to original order before converting it to a UUID
     • wid(wid_str, keep_order=True) - overrides default behavior of reordering the WID string before conversion
          [keep_order works with all param options]

    if keep_order == False (default: False) we reorder the WID string
    back to its original order before converting it back to the original UUID
    used to create this WID
    
    for each WID keep_order should have the same value 
    when creating a WID and converting a WID back to a UUID 
    it is up to the coder to keep track of WID keep_order usage
    easiest thing to do is just use the default and you should be good
    """
    if keep_order == False:
        w = w[:9][::-1] + w[9:22]
    # '===' triple equal sign padding works with any 64 bit encoded unpadded string
    # whether you need them or not
    return UUID(bytes=urlsafe_b64decode(w + '==='))
