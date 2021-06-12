import {trigger, stagger, animate, style, group, query, transition, keyframes} from '@angular/animations';
// const query = (s:any,a:any,o={optional:true})=>q(s,a,o);

// define add edit page animation or page transitions
export const AddEditTransition = trigger('AddEditTransition', [
  transition(':enter', [
    query('.right-part', style({ opacity: 0 })),
    query('.right-part', stagger(300, [
      style({ transform: 'scale(1,0)' }),
      animate('1.5s cubic-bezier(.75,-0.48,.26,1.52)', style({transform: 'scale(1,1)', opacity: 1})),
    ])),
  ]),
  transition(':leave', [
    query('.right-part', stagger(300, [
      // style({ transform: 'translateX(0%)', opacity: 1 }),
      //  animate('0.6s ease-in-out', style({ transform: 'translateX(-100%)', overflow: 'hidden', opacity: 0 }))

      style({ transform: 'translate(0,0)', opacity: 1 }),
      animate('.1s cubic-bezier(.75,-0.48,.26,1.52)', style({ opacity: 0})),
    ])),        
  ])
]);

// define add edit steps page animation or page transitions
export const AddEditStepFlipTransition = trigger('AddEditStepFlipTransition', [
  transition(':enter', [
    query('.box,.table-list,.universalbox', style({ opacity: 0 })),
    query('.box,.table-list,.universalbox', stagger(300, [
      style({ transform: 'rotateY(180deg)' }),
      animate('1.5s cubic-bezier(.75,-0.48,.26,1.52)', style({transform: 'rotateY(0deg)', opacity: 1})),
    ])),
  ]),
  transition(':leave', [
    query('.box,.table-list,.universalbox', stagger(300, [
      
      style({ transform: 'rotateY(0deg)', opacity: 1 }),
      animate('.1s cubic-bezier(.75,-0.48,.26,1.52)', style({ transform: 'rotateY(180deg)', opacity: 0})),
    ])),        
  ])

  
]);

// define add edit steps page animation or page transitions
// export const AddEditStepSlideTransition = trigger('AddEditStepTransition', [
//   transition(':enter', [
//     query('.body-part', style({ opacity: 0 })),
//     query('.body-part', stagger(300, [
//       style({ transform: 'translate(-50%,-40%)' }),
//         animate('1s cubic-bezier(.75,-0.48,.26,1.52)', style({transform: 'translate(-50%,-50%)', opacity: 1})),
//     ])),
//   ]),
//   transition(':leave', [
//     query('.body-part', stagger(300, [
      
//       style({ transform: 'translate(-50%,-50%)', opacity: 1 }),
//         animate('.8s cubic-bezier(.75,-0.48,.26,1.52)', style({transform: 'translate(-50%,-70%)', opacity: 0})),
//     ])),        
//   ])
// ]);
