
import { Directive, ElementRef, Renderer,HostListener } from '@angular/core';

@Directive({ selector: '[accordianBox]' })
export class AccordianDirective {

    constructor(public el: ElementRef, public renderer: Renderer) {}

    @HostListener('click') onClick() {

        var all_boxs = document.querySelectorAll('.boxs');        
        for (var i = 0, len = all_boxs.length; i < len; i++) {
            this.renderer.setElementClass(all_boxs[i], 'active', false);
            this.renderer.setElementClass(all_boxs[i].querySelector('.acc_icon'), 'icon-addsvg', true);
            this.renderer.setElementClass(all_boxs[i].querySelector('.acc_icon'), 'icon-minus', false);
        }
        
        this.renderer.setElementClass(this.el.nativeElement, 'active', true);
        this.renderer.setElementClass(this.el.nativeElement.querySelector('.acc_icon'), 'icon-addsvg', false);
        this.renderer.setElementClass(this.el.nativeElement.querySelector('.acc_icon'), 'icon-minus', true);
    }

    ngOnInit(){
        // Use renderer to render the emelemt with styles
        
        var all_boxs = document.querySelectorAll('.boxs');        
        this.renderer.setElementClass(all_boxs[0], 'active', true);
        
    }
}