import { TestBed, inject } from '@angular/core/testing';

import { KalService } from './kal.service';

describe('KalService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [KalService]
    });
  });

  it('should be created', inject([KalService], (service: KalService) => {
    expect(service).toBeTruthy();
  }));
});
