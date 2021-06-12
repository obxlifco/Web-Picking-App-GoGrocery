import {trigger, stagger, animate, style, group, query, transition, keyframes} from '@angular/animations';

// define add edit steps page animation or page transitions
export const ProdListTransition = trigger('ProdListTransition', [
  transition('* => *', [
    // this hides everything right away
    query(':enter', style({ opacity: 0, transform: 'translateY(50%)' }),{ optional: true }),
    
    // starts to animate things with a stagger in between
    query(':enter', stagger('100ms', [
      		animate('1s', style({ opacity: 1, transform: 'translateY(0)' }))
    	]),{ optional: true })
  ])
]);

