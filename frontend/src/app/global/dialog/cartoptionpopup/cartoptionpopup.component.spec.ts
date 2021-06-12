import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CartoptionpopupComponent } from './cartoptionpopup.component';

describe('CartoptionpopupComponent', () => {
  let component: CartoptionpopupComponent;
  let fixture: ComponentFixture<CartoptionpopupComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CartoptionpopupComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CartoptionpopupComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
