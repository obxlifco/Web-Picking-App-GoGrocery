import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CreditburnComponent } from './creditburn.component';

describe('CreditburnComponent', () => {
  let component: CreditburnComponent;
  let fixture: ComponentFixture<CreditburnComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CreditburnComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CreditburnComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
