-- Table: public.index

-- DROP TABLE IF EXISTS public.index;

CREATE TABLE IF NOT EXISTS public.index
(
    docnum integer NOT NULL,
    term character varying COLLATE pg_catalog."default" NOT NULL,
    count integer,
    CONSTRAINT "Index_pkey" PRIMARY KEY (docnum),
    CONSTRAINT "Index_docNum_fkey" FOREIGN KEY (docnum)
        REFERENCES public.documents (docnum) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT "Index_term_fkey" FOREIGN KEY (term)
        REFERENCES public.terms (term) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.index
    OWNER to postgres;