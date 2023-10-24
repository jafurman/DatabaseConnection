-- Table: public.documents

-- DROP TABLE IF EXISTS public.documents;

CREATE TABLE IF NOT EXISTS public.documents
(
    docnum integer NOT NULL,
    text character varying COLLATE pg_catalog."default" NOT NULL,
    title character varying COLLATE pg_catalog."default" NOT NULL,
    numchars integer NOT NULL,
    category_id integer NOT NULL,
    date character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "Documents_pkey" PRIMARY KEY (docnum),
    CONSTRAINT "Documents_category_Id_fkey" FOREIGN KEY (category_id)
        REFERENCES public.categories (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.documents
    OWNER to postgres;