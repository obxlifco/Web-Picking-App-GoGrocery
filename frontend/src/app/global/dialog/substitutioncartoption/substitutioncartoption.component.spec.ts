import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SubstitutioncartoptionComponent } from './substitutioncartoption.component';

describe('SubstitutioncartoptionComponent', () => {
  let component: SubstitutioncartoptionComponent;
  let fixture: ComponentFixture<SubstitutioncartoptionComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SubstitutioncartoptionComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SubstitutioncartoptionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
