#!/usr/bin/env python



class VlcOperator:
    """Execute mb.youtube() search using the less-than operator.
       Remembers the last mediabyte."""
    def __lt__(self, other):            # youtube search with <
        self.mixtape = Convert.search_to_mixtape(other)
        self.omm = self.mixtape.omm_oneline()
        Convert.search_to_mixtape(other).vlc()
                                        # subtitle search with //
    def __floordiv__(self, subtitle_search):
        subtitleMix = self.mixtape.srt_search(subtitle_search)
        return subtitleMix
    
    def __truediv__(self, subtitle_search):
        subtitleMix = self.mixtape.srt_search(subtitle_search, sample_length=0)
        return subtitleMix
    
    def __str__(self):
        return self.mixtape.__str__()
                               # call mixtape methods dynamically
    def method(self, method_name, *args):
        mb_obj = Convert.omm(self.omm)
        func = getattr(mb_obj, method_name)
        return func(*args)
    def eject(self):
        return self.mixtape