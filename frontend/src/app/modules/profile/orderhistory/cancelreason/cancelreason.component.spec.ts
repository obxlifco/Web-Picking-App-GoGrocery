import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CancelreasonComponent } from './cancelreason.component';

describe('CancelreasonComponent', () => {
  let component: CancelreasonComponent;
  let fixture: ComponentFixture<CancelreasonComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CancelreasonComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CancelreasonComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
