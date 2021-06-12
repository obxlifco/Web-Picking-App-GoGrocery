import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FailepaymentComponent } from './failepayment.component';

describe('FailepaymentComponent', () => {
  let component: FailepaymentComponent;
  let fixture: ComponentFixture<FailepaymentComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FailepaymentComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FailepaymentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
