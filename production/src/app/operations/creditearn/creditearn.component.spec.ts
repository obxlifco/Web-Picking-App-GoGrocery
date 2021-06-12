import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CreditearnComponent } from './creditearn.component';

describe('CreditearnComponent', () => {
  let component: CreditearnComponent;
  let fixture: ComponentFixture<CreditearnComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CreditearnComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CreditearnComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
