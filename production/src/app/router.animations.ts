import {trigger, animate, style, group, query, transition} from '@angular/animations';

// define route change animation or page transitions
export const routerTransition = trigger('routerTransition', [
  transition('* <=> *', [
    query(':enter, :leave', style({ position: 'fixed', width:'100%' })
      , { optional: true }),
    group([
      query(':enter', [
        style({ transform: 'translateX(100%)' , opacity: 0.5 }),
        animate('0.8s ease-in-out', style({ transform: 'translateX(0%)', opacity: 1 }))
      ], { optional: true }),
      query(':leave', [
        style({ transform: 'translateX(0%)', opacity: 1 }),
        animate('0.6s ease-in-out', style({ transform: 'translateX(-100%)', overflow: 'hidden', opacity: 0 }))
      ], { optional: true }),
    ])
  ])
])

// define addedit page animation or page transitions
export const AddEditTransition = trigger('AddEditTransition', [
  transition('* <=> *', [
    query(':enter, :leave', style({  width:'100%' })
      , { optional: true }),
    group([
      query(':enter', [
        style({ transform: 'translate(-50%,-40%)' }),
        animate('1s cubic-bezier(.75,-0.48,.26,1.52)', style({transform: 'translate(-50%,-50%)', opacity: 1})),
      ], { optional: true }),
      query(':leave', [
        style({ transform: 'translate(-50%,-50%)', opacity: 1 }),
        animate('.8s cubic-bezier(.75,-0.48,.26,1.52)', style({transform: 'translate(-50%,-70%)', opacity: 0})),
      ], { optional: true }),
    ])
  ])
])


