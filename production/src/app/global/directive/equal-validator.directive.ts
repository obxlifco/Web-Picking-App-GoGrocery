import { Directive, forwardRef, Attribute } from '@angular/core';
import { NG_VALIDATORS, Validator, Validators, AbstractControl, ValidatorFn } from '@angular/forms';

@Directive({
    selector: '[validateEqual][formControlName],[validateEqual][formControl],[validateEqual][ngModel]',
    providers: [{ provide: NG_VALIDATORS, useExisting: forwardRef(() => EqualValidator), multi: true }]
})

export class EqualValidator implements Validator {
    constructor( @Attribute('validateEqual') public validateEqual: string) {}

    validate(c: AbstractControl): { [key: string]: any } {
        // self value (e.g. retype password)
        let v = c.value;

        // control value (e.g. password)
        let e = c.root.get(this.validateEqual);

        // value not equal
        if (e && v !== e.value) return {
            validateEqual: false
        }
        return null;
    }
}



@Directive({
    selector: '[validateSafe][formControlName],[validateSafe][formControl],[validateSafe][ngModel]',
    providers: [{ provide: NG_VALIDATORS, useExisting: forwardRef(() => SafeValidator), multi: true }]
})

export class SafeValidator implements Validator {
    constructor( @Attribute('validateSafe') public validateSafe: string) {}

    validate(c: AbstractControl): { [key: string]: any } {
        // self value 
        let v = c.value;
        let patt = new RegExp("^[ A-Za-z0-9_\x27\x22@./#&%+-]*$");

        // value not equal
        if (!patt.test(v)) return {
            validateSafe: false
        }
        return null;
    }
}


@Directive({
    selector: '[validatePassword][formControlName],[validatePassword][formControl],[validatePassword][ngModel]',
    providers: [{ provide: NG_VALIDATORS, useExisting: forwardRef(() => passwordValidator), multi: true }]
})

export class passwordValidator implements Validator {
    constructor( @Attribute('validatePassword') public validatePassword: any) {}

    validate(c: AbstractControl): { [key: string]: any } {
        // self value (e.g. retype password)
        let v = c.value;
        
        let pwdValidLength = (v && v.length >= 8 ? true : false);
        let pwdHasCapLetter = (v && /[A-Z]/.test(v)) ? true : false;
        let pwdHaslowLetter = (v && /[a-z]/.test(v)) ? true : false;
        let pwdHasSplChar = (v && /[#?!@$%^&*-]/.test(v)) ? true : false;
        let pwdHasNumber = (v && /[0-9]/.test(v)) ? true : false;

        if(!pwdValidLength || !pwdHasCapLetter || !pwdHaslowLetter || !pwdHasNumber || !pwdHasSplChar) return {
            validatePassword: { len: pwdValidLength, cap: pwdHasCapLetter, low: pwdHaslowLetter, num: pwdHasNumber, spl: pwdHasSplChar  }
        }
        
        return null;
       
    }


}


@Directive({
    selector: '[validateMin][formControlName],[validateMin][formControl],[validateMin][ngModel]',
    providers: [{ provide: NG_VALIDATORS, useExisting: forwardRef(() => MinValidator), multi: true }]
})

export class MinValidator implements Validator {
    constructor( @Attribute('validateMin') public validateMin: string) {}

    validate(c: AbstractControl): { [key: string]: any } {
        // self value 
        let v = c.value;

        // control value (e.g. min value)
        let e = this.validateMin;
        // value not equal
        if (v < e) return {
            validateMin: false
        }
        return null;
    }
}

@Directive({
    selector: '[validateMax][formControlName],[validateMax][formControl],[validateMax][ngModel]',
    providers: [{ provide: NG_VALIDATORS, useExisting: forwardRef(() => MaxValidator), multi: true }]
})

export class MaxValidator implements Validator {
    constructor( @Attribute('validateMax') public validateMax: string) {}

    validate(c: AbstractControl): { [key: string]: any } {
        // self value 
        let v = c.value;

        // control value (e.g. max value)
        let e = this.validateMax;

        // value not equal
        if (v > e) return {
            validateMax: false
        }
        return null;
    }
}