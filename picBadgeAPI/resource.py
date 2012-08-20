import json

from piston.decorator import decorator
from piston.resource import Resource
from piston.utils import rc, FormValidationError

def validate(v_form, operation="POST"):
    
    @decorator
    def wrap(f, self, request, *a, **kwa):
        form = v_form(request.data)
        
        if form.is_valid():
            setattr(request, 'form', form)
            return f(self, request, *a, **kwa)
        else:
        	#setattr(request, 'form', form)
        	#return f(self, request, *a, **kwa)            
            raise FormValidationError(form)
    return wrap


class Resource(Resource):
    
    def form_validation_response(selfself, e):
        resp = rc.BAD_REQUEST
        
        json_errors = json.dumps(
            dict(
                 (k, map(unicode, v))
                 for (k,v) in e.form.errors.iteritems()
            )
        )
        resp.write(json_errors)
        return resp