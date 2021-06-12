import { TestBed } from '@angular/core/testing';

import { UtillService } from './utill.service';

describe('UtillService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: UtillService = TestBed.get(UtillService);
    expect(service).toBeTruthy();
  });
});
