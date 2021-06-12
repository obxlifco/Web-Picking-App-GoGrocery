import { TestBed } from '@angular/core/testing';

import { DealsorsellService } from './dealsorsell.service';

describe('DealsorsellService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: DealsorsellService = TestBed.get(DealsorsellService);
    expect(service).toBeTruthy();
  });
});
